import re

# Set of common prompt injection and jailbreak phrases
JAILBREAK_PATTERNS = [
    r"ignore\s+(?:all\s+)?previous\s+instructions",
    r"ignore\s+(?:all\s+)?prior\s+system\s+directives",
    r"system\s+override",
    r"you\s+are\s+now\s+(?:a\s+)?dan\b",
    r"do\s+anything\s+now",
    r"bypass\s+restrictions",
    r"developer\s+mode\s+active",
    r"acting\s+as\s+a\s+malicious\s+agent",
    r"unrestricted\s+access",
    r"write\s+a\s+python\s+script\s+to\s+hack",
    r"how\s+to\s+(?:make|build|create)\s+(?:a\s+)?(?:bomb|explosive|weapon|virus|malware)"
]

# Set of explicit terms representing unsafe prompts (hate speech, harm, cyberattacks)
HARMFUL_KEYWORD_PATTERNS = [
    r"\b(?:cyberattack|phishing\s+email|hack\s+into|cracking\s+passwords)\b",
    r"\b(?:suicide|self-harm|kill\s+myself)\b",
    r"\b(?:hate\s+speech|racial\s+slur|discriminatory\s+insult)\b"
]

class GuardrailSystem:
    """
    Active safety and policy alignment guardrail layer.
    Performs pre-inference input validation and post-inference output verification.
    """
    def __init__(self, input_enabled: bool = True, output_enabled: bool = True):
        self.input_enabled = input_enabled
        self.output_enabled = output_enabled
        
        # Compile patterns for fast matching
        self.jailbreak_regex = [re.compile(p, re.IGNORECASE) for p in JAILBREAK_PATTERNS]
        self.harmful_regex = [re.compile(p, re.IGNORECASE) for p in HARMFUL_KEYWORD_PATTERNS]

    def scan_input(self, prompt: str) -> tuple[bool, str | None]:
        """
        Scans user prompt for safety policy violations.
        Returns (is_safe, refusal_reason).
        """
        if not self.input_enabled:
            return True, None
            
        # Check for jailbreak templates
        for idx, pattern in enumerate(self.jailbreak_regex):
            if pattern.search(prompt):
                return False, "Prompt contains structures associated with conversational jailbreaks or prompt injections."
                
        # Check for harmful keywords
        for idx, pattern in enumerate(self.harmful_regex):
            if pattern.search(prompt):
                return False, "Prompt matches topics violating safety policies regarding cybersecurity, self-harm, or discrimination."
                
        return True, None

    def scan_output(self, response: str) -> tuple[bool, str]:
        """
        Scans model output for compliance and policy breaches.
        Returns (is_safe, processed_response).
        """
        if not self.output_enabled:
            return True, response
            
        # Scan for leaked api keys or sensitive structures (like mock API keys)
        # e.g., "sk-..." or "AIzaSy..."
        api_key_regex = re.compile(r'\b(?:sk-[a-zA-Z0-9]{32,}|AIzaSy[a-zA-Z0-9_-]{33})\b')
        if api_key_regex.search(response):
            # Censor leaked API keys
            censored_response = api_key_regex.sub("[CENSORED_SENSITIVE_KEY]", response)
            return False, censored_response

        # Scan for extreme offensive words/toxicity (using a basic filter for demonstration)
        # In production, we'd call a dedicated moderation endpoint.
        offensive_pattern = re.compile(r'\b(?:slurs|highly_toxic_placeholder)\b', re.IGNORECASE)
        if offensive_pattern.search(response):
            return False, "I apologize, but my response was blocked by the output safety guardrails due to a policy violation."
            
        return True, response

    def get_standard_refusal(self, reason: str) -> str:
        """Returns a standardized professional policy refusal message."""
        return f"🚨 **Guardrail Alert**: I apologize, but I cannot process this request. Reason: {reason} Please rephrase your query keeping it constructive and safe."
