import time
import os
import requests
from huggingface_hub import InferenceClient
from app.memory import ConversationMemory
from app.guardrails import GuardrailSystem
from app.tools import get_tools_system_prompt, parse_and_execute_tool
from app.observability import TelemetryLogger

class OpenSourceAssistant:
    """
    Open Source Personal Assistant powered by Hugging Face's serverless Inference API.
    Supports memory, active guardrails, tools, and latency/cost telemetry.
    """
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        hf_token: str = None,
        memory_window: int = 10,
        guardrails_enabled: bool = True
    ):
        self.model_name = model_name
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")
        self.memory = ConversationMemory(window_size=memory_window)
        self.guardrails = GuardrailSystem(input_enabled=guardrails_enabled, output_enabled=guardrails_enabled)
        self.logger = TelemetryLogger()
        self.system_prompt = "You are a helpful, secure, and precise Open Source AI assistant. You answer queries factually and assist the user."

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
                model_type=f"oss_{self.model_name.split('/')[-1].lower()}",
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
            
        formatted_messages = self.memory.get_messages_for_api(include_system=full_system_prompt)
        
        tool_used_name = None
        assistant_reply = ""
        
        try:
            # Initialize Hugging Face Inference Client
            # Note: client falls back to unauthenticated public endpoint if token is None,
            # but is heavily rate-limited.
            client = InferenceClient(model=self.model_name, token=self.hf_token)
            
            # Make API Call
            hf_response = client.chat_completion(
                messages=formatted_messages,
                max_tokens=1024,
                temperature=0.3
            )
            
            assistant_reply = hf_response.choices[0].message.content
            
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
                    new_messages = self.memory.get_messages_for_api(include_system=full_system_prompt)
                    hf_response_2 = client.chat_completion(
                        messages=new_messages,
                        max_tokens=1024,
                        temperature=0.2
                    )
                    assistant_reply = hf_response_2.choices[0].message.content
            
        except Exception as e:
            # If serverless inference fails, provide a descriptive error response
            assistant_reply = f"Error: Unable to connect to Hugging Face serverless API for model '{self.model_name}'. Details: {str(e)}"
            if "Authorization" in assistant_reply or "401" in assistant_reply:
                assistant_reply += "\n\n💡 *Tip: Please double-check your Hugging Face API Token (HF_TOKEN) in the sidebar.*"
        
        # 3. Post-inference output guardrail check
        output_safe, censored_reply = self.guardrails.scan_output(assistant_reply)
        final_reply = censored_reply
        
        # Add assistant reply to memory
        self.memory.add_assistant_message(final_reply)
        
        # Telemetry calculation
        latency_ms = (time.time() - start_time) * 1000
        
        # Qwen 2.5 7B serverless pricing is typically extremely low (or free).
        # We'll use a standard cost estimate: $0.07 per 1M tokens ($0.00000007 per token)
        in_tokens = len(str(formatted_messages)) // 4
        out_tokens = len(final_reply) // 4
        cost_estimate = (in_tokens + out_tokens) * 0.00000007
        
        guardrail_tripped_int = 1 if not output_safe else 0
        guardrail_reason_str = "Sensitive output censored (e.g. API keys detected)" if not output_safe else None

        self.logger.log_interaction(
            model_type=f"oss_{self.model_name.split('/')[-1].lower()}",
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
