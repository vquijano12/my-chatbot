class ConversationManager:
    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({"role": "user", "content": message})

    def add_assistant_message(self, message):
        self.history.append({"role": "assistant", "content": message})

    def get_history(self):
        return self.history

    def build_prompt(self, context=None):
        prompt = ""
        for turn in self.history:
            if turn["role"] == "user":
                prompt += f"User: {turn['content']}\n"
            else:
                prompt += f"Assistant: {turn['content']}\n"
        if context:
            prompt += f"\nContext:\n{context}\n"
        prompt += "Assistant:"
        return prompt
