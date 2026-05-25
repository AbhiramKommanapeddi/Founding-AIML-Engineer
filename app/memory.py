class ConversationMemory:
    """
    Manages conversational memory for the AI assistants.
    Supports conversational history tracking, sliding window limits,
    and history serialization.
    """
    def __init__(self, window_size: int = 10):
        self.messages = []  # List of dict: {"role": "user"|"assistant"|"system", "content": str}
        self.window_size = window_size
        self.summary = ""

    def add_message(self, role: str, content: str):
        """Adds a message to the raw conversational history."""
        self.messages.append({"role": role, "content": content})

    def add_user_message(self, content: str):
        self.add_message("user", content)

    def add_assistant_message(self, content: str):
        self.add_message("assistant", content)

    def add_system_message(self, content: str):
        self.add_message("system", content)

    def get_messages_for_api(self, include_system: str = None) -> list:
        """
        Returns a list of messages formatted for model APIs.
        Applies a sliding window of the last `window_size` turns (user + assistant pairs).
        Includes the system prompt if provided.
        """
        formatted = []
        if include_system:
            formatted.append({"role": "system", "content": include_system})
            
        # Sliding window: 1 window turn = 1 user + 1 assistant message = 2 messages
        max_messages = self.window_size * 2
        recent_messages = self.messages[-max_messages:] if max_messages > 0 else self.messages
        
        # If there is an active summary of older history, prepend it
        if self.summary:
            summary_msg = f"[Summary of previous conversation: {self.summary}]"
            # Prepend to the first user message or as a system note
            formatted.append({"role": "system", "content": summary_msg})

        formatted.extend(recent_messages)
        return formatted

    def clear(self):
        """Clears all conversation memory."""
        self.messages = []
        self.summary = ""

    def get_raw_history(self) -> list:
        """Returns the complete un-truncated history."""
        return self.messages

    def set_summary(self, summary_text: str):
        """Sets a summary of the older conversational history."""
        self.summary = summary_text

    def to_dict(self) -> dict:
        """Serializes the memory state."""
        return {
            "messages": self.messages,
            "window_size": self.window_size,
            "summary": self.summary
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserializes memory state from a dictionary."""
        memory = cls(window_size=data.get("window_size", 10))
        memory.messages = data.get("messages", [])
        memory.summary = data.get("summary", "")
        return memory
