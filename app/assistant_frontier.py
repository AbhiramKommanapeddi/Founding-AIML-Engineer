import time
import os
import google.generativeai as genai
from app.memory import ConversationMemory
from app.guardrails import GuardrailSystem
from app.tools import get_tools_system_prompt, parse_and_execute_tool
from app.observability import TelemetryLogger

class FrontierAssistant:
    """
    Frontier AI Assistant powered by Google's Gemini API.
    Supports memory, active guardrails, tools, and latency/cost telemetry.
    """
    def __init__(
        self,
        model_name: str = "gemini-1.5-flash",
        api_key: str = None,
        memory_window: int = 10,
        guardrails_enabled: bool = True
    ):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.memory = ConversationMemory(window_size=memory_window)
        self.guardrails = GuardrailSystem(input_enabled=guardrails_enabled, output_enabled=guardrails_enabled)
        self.logger = TelemetryLogger()
        self.system_prompt = "You are a helpful, secure, and precise Frontier AI assistant. You answer queries factually and assist the user."

    def _format_messages_for_gemini(self, messages: list) -> list:
        """
        Translates role/content dictionary list to Gemini contents format.
        Maps 'assistant' role to 'model'.
        Excludes system messages because we pass system instructions separately in the config.
        """
        gemini_contents = []
        for msg in messages:
            if msg["role"] == "system":
                continue
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        return gemini_contents

    def generate_response(self, user_prompt: str, use_tools: bool = True) -> dict:
        """
        Processes a user prompt, applies guardrails, handles multi-turn memory,
        executes tools if needed, logs telemetry, and returns the response.
        
        Returns:
            dict containing: "response" (str), "latency_ms" (float), "guardrail_tripped" (bool), "tool_used" (str|None)
        """
        start_time = time.time()
        
        # 1. Pre-inference input guardrail check
        is_safe, refusal_reason = self.guardrails.scan_input(user_prompt)
        if not is_safe:
            refusal_response = self.guardrails.get_standard_refusal(refusal_reason)
            self.memory.add_user_message(user_prompt)
            self.memory.add_assistant_message(refusal_response)
            
            latency_ms = (time.time() - start_time) * 1000
            self.logger.log_interaction(
                model_type=f"frontier_{self.model_name.replace('-', '_')}",
                prompt=user_prompt,
                response=refusal_response,
                latency_ms=latency_ms,
                tokens_input=len(user_prompt) // 4,
                tokens_output=len(refusal_response) // 4,
                cost_usd=0.0,
                guardrail_tripped=1,
                guardrail_reason=refusal_reason
            )
            return {
                "response": refusal_response,
                "latency_ms": latency_ms,
                "guardrail_tripped": True,
                "tool_used": None
            }

        # Add user prompt to memory
        self.memory.add_user_message(user_prompt)
        
        # Combine system prompt with tools instructions if enabled
        full_system_prompt = self.system_prompt
        if use_tools:
            full_system_prompt += "\n\n" + get_tools_system_prompt()
            
        tool_used_name = None
        assistant_reply = ""
        
        try:
            # Configure API key
            if not self.api_key:
                raise ValueError("Gemini API Key is missing. Please set GEMINI_API_KEY in the environment or Streamlit sidebar.")
                
            genai.configure(api_key=self.api_key)
            
            # Setup model with system instructions
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=full_system_prompt,
                generation_config={"temperature": 0.2}
            )
            
            # Formulate history from memory
            raw_history = self.memory.get_messages_for_api()
            gemini_contents = self._format_messages_for_gemini(raw_history)
            
            # Make API Call
            gemini_response = model.generate_content(gemini_contents)
            assistant_reply = gemini_response.text
            
            # 2. Check for Tool Use XML Tags in model reply
            if use_tools:
                tool_check = parse_and_execute_tool(assistant_reply)
                if tool_check["has_call"]:
                    tool_used_name = tool_check["name"]
                    # Add model's intermediate tool call to memory
                    self.memory.add_assistant_message(assistant_reply)
                    
                    # Create tool response message
                    tool_response_content = f"<tool_response>{tool_check['result']}</tool_response>"
                    self.memory.add_message("user", tool_response_content)
                    
                    # Run second inference turn with tool results included in context
                    new_history = self.memory.get_messages_for_api()
                    new_gemini_contents = self._format_messages_for_gemini(new_history)
                    
                    gemini_response_2 = model.generate_content(new_gemini_contents)
                    assistant_reply = gemini_response_2.text
            
        except Exception as e:
            assistant_reply = f"Error: Unable to connect to Google Gemini API for model '{self.model_name}'. Details: {str(e)}"
            if "key" in assistant_reply.lower() or "api_key" in assistant_reply.lower() or "400" in assistant_reply:
                assistant_reply += "\n\n💡 *Tip: Please double-check your Gemini API Key in the sidebar.*"
        
        # 3. Post-inference output guardrail check
        output_safe, censored_reply = self.guardrails.scan_output(assistant_reply)
        final_reply = censored_reply
        
        # Add assistant reply to memory
        self.memory.add_assistant_message(final_reply)
        
        # Telemetry calculation
        latency_ms = (time.time() - start_time) * 1000
        
        # Gemini 1.5 Flash Pricing: Input: $0.075 / 1M tokens ($0.000000075 / token), Output: $0.30 / 1M tokens ($0.00000030 / token)
        in_tokens = len(str(gemini_contents)) // 4
        out_tokens = len(final_reply) // 4
        cost_estimate = (in_tokens * 0.000000075) + (out_tokens * 0.000000300)
        
        guardrail_tripped_int = 1 if not output_safe else 0
        guardrail_reason_str = "Sensitive output censored (e.g. API keys detected)" if not output_safe else None

        self.logger.log_interaction(
            model_type=f"frontier_{self.model_name.replace('-', '_')}",
            prompt=user_prompt,
            response=final_reply,
            latency_ms=latency_ms,
            tokens_input=in_tokens,
            tokens_output=out_tokens,
            cost_usd=cost_estimate,
            guardrail_tripped=guardrail_tripped_int,
            guardrail_reason=guardrail_reason_str
        )
        
        return {
            "response": final_reply,
            "latency_ms": latency_ms,
            "guardrail_tripped": not output_safe,
            "tool_used": tool_used_name
        }
