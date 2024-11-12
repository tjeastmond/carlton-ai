from abc import ABC, abstractmethod


class ChatInterface(ABC):
    @abstractmethod
    def hello(self) -> str:
        pass

    @abstractmethod
    def chat(self, input_text: str) -> str:
        pass


class OpenAi(ChatInterface):
    def hello(self) -> str:
        return "Hello from OpenAi!"

    def chat(self, input_text: str) -> str:
        # Process the input text here
        return f"OpenAi response to {input_text}"


class Llama(ChatInterface):
    def hello(self) -> str:
        return "Hello from Llama!"

    def chat(self, input_text: str) -> str:
        # Process the input text here
        return f"LlAMA Chat response to {input_text}"


class AI_Bots:
    def __init__(self):
        self.bots = {
            "OpenAi": OpenAi(),
            "Llama": Llama(),
        }

    def get_bot(self, bot_name: str) -> ChatInterface:
        if bot_name in self.bots:
            return self.bots[bot_name]
        else:
            raise ValueError(f"Unknown AI bot: {bot_name}")


def get_ai_bot(bot_name: str):
    ai_bots = AI_Bots()

    try:
        return ai_bots.get_bot(bot_name)

    except ValueError as e:
        print(e)
        return None
