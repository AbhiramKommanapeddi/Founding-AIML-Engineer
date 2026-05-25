import datetime
import math
import re
import json

def get_current_time(*args, **kwargs) -> str:
    """Returns the current local date and time."""
    now = datetime.datetime.now()
    return f"The current local date and time is: {now.strftime('%A, %B %d, %Y, %I:%M %p')}"

def calculate_expression(expression: str, *args, **kwargs) -> str:
    """
    Securely evaluates a mathematical expression containing numbers, operators, and basic math functions.
    Allowed operators: +, -, *, /, **, %, (, )
    Allowed functions: sin, cos, tan, sqrt, log, exp, pi, e
    """
    # Clean expression
    expr = expression.strip().lower()
    
    # Safety whitelist regex pattern to prevent arbitrary code execution
    # Only allow digits, spaces, standard operators, parentheses, and white-listed math words
    allowed_pattern = re.compile(r'^[0-9\s\+\-\*\/\%\(\)\.\,]|(sin|cos|tan|sqrt|log|exp|pi|e|\*\*)+$')
    
    # Remove whitespace
    expr_clean = expr.replace(" ", "")
    
    # Validate character whitelist
    safe_chars = re.match(r'^[0-9\+\-\*\/\(\)\.\%\s\*\*a-z,]+$', expr_clean)
    if not safe_chars:
        return "Error: Expression contains unsafe characters."
        
    # Extra validation for allowed words
    words = re.findall(r'[a-z]+', expr_clean)
    for word in words:
        if word not in {"sin", "cos", "tan", "sqrt", "log", "exp", "pi", "e"}:
            return f"Error: Function '{word}' is not allowed for security reasons."

    # Define safe evaluation context
    safe_dict = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "__builtins__": None
    }
    
    try:
        # Secure eval with no builtins and safe math dictionary
        result = eval(expr_clean, {"__builtins__": None}, safe_dict)
        return f"Result of '{expression}': {result}"
    except Exception as e:
        return f"Error evaluating mathematical expression: {str(e)}"

# Mock database for search
WIKIPEDIA_DATABASE = {
    "qwen": "Qwen is a series of large language models developed by Alibaba Cloud. The models are open-source and trained on vast datasets, excelling in reasoning, coding, and multilingual tasks.",
    "gemini": "Gemini is a family of highly capable multimodal AI models developed by Google, spanning Nano, Flash, Pro, and Ultra sizes, designed to natively understand text, code, images, audio, and video.",
    "deepmind": "Google DeepMind is a pioneer in artificial intelligence, responsible for landmarks like AlphaGo, AlphaFold, and co-creating Google's flagship Gemini models.",
    "hugging face": "Hugging Face is a collaboration platform for the machine learning community, best known for its transformers library and hosting open-source models, datasets, and web spaces.",
    "ai safety": "AI safety is an interdisciplinary field focused on ensuring that artificial intelligence systems behave alignly with human values and intentions, preventing harmful or catastrophic outcomes.",
    "hallucination": "An AI hallucination is a phenomenon where a large language model generates highly confident but factually incorrect or ungrounded statements.",
    "guardrails": "AI Guardrails are active software safety layers placed around LLMs to validate input prompts for policy compliance and filter output responses to prevent harmful generations."
}

def search_wikipedia_mock(query: str, *args, **kwargs) -> str:
    """Searches a mock knowledge base for encyclopedic facts."""
    q = query.strip().lower()
    
    # Try exact match or substring match
    results = []
    for key, value in WIKIPEDIA_DATABASE.items():
        if key in q or q in key:
            results.append(f"[{key.title()}]: {value}")
            
    if results:
        return "\n\n".join(results)
    return f"No direct search results found in mock database for '{query}'. Try searching for: Qwen, Gemini, DeepMind, Hugging Face, AI Safety, Hallucination, or Guardrails."

# Tool Registry
TOOL_REGISTRY = {
    "get_current_time": {
        "func": get_current_time,
        "description": "get_current_time() -> Returns the current local date and time."
    },
    "calculate_expression": {
        "func": calculate_expression,
        "description": "calculate_expression(expression: str) -> Evaluates a safe mathematical expression. Example: calculate_expression('sqrt(256) * 12')"
    },
    "search_wikipedia_mock": {
        "func": search_wikipedia_mock,
        "description": "search_wikipedia_mock(query: str) -> Queries a factual mock database for definitions and information."
    }
}

def get_tools_system_prompt() -> str:
    """Generates the instructions for assistants to use tools."""
    prompt = "You have access to the following tools to assist the user:\n\n"
    for name, info in TOOL_REGISTRY.items():
        prompt += f"- {name}: {info['description']}\n"
    prompt += """
To use a tool, format your thought and call exactly like this:
Thought: I need to use the calculate_expression tool to find the result of 15 * 24.
<tool_call name="calculate_expression">15 * 24</tool_call>

Once the tool execution response is provided back to you as:
<tool_response>Result of '15 * 24': 360</tool_response>

You must write your final answer using that information. DO NOT hallucinate answers that require tools.
"""
    return prompt

def parse_and_execute_tool(response_text: str) -> dict:
    """
    Parses a model response to detect any `<tool_call>` tags.
    If found, executes the tool and returns details.
    
    Returns:
        dict with keys: "has_call" (bool), "name" (str), "args" (str), "result" (str), "error" (str)
    """
    # Pattern to find: <tool_call name="tool_name">arguments</tool_call>
    match = re.search(r'<tool_call\s+name="([^"]+)"\s*>(.*?)</tool_call>', response_text, re.DOTALL)
    if not match:
        return {"has_call": False}
        
    tool_name = match.group(1).strip()
    tool_args = match.group(2).strip()
    
    if tool_name not in TOOL_REGISTRY:
        return {
            "has_call": True,
            "name": tool_name,
            "args": tool_args,
            "result": f"Error: Tool '{tool_name}' is not registered.",
            "error": True
        }
        
    try:
        func = TOOL_REGISTRY[tool_name]["func"]
        result = func(tool_args)
        return {
            "has_call": True,
            "name": tool_name,
            "args": tool_args,
            "result": result,
            "error": False
        }
    except Exception as e:
        return {
            "has_call": True,
            "name": tool_name,
            "args": tool_args,
            "result": f"Error executing tool '{tool_name}': {str(e)}",
            "error": True
        }
