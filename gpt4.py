import openai
import os
from dotenv import load_dotenv
import asyncio
from tiktoken import get_encoding

load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self, model="gpt-4"):
        self.model = model
        try:
            self.encoding = get_encoding(self.model)
        except ValueError:
            print("Warning: model not found. Using cl100k_base encoding.")
            self.encoding = get_encoding("cl100k_base")

    async def _call_openai(self, messages, instruction=None):
        if instruction:
            messages.insert(0, {"role": "system", "content": instruction})
        completion = await asyncio.to_thread(
            openai.ChatCompletion.create, model=self.model, messages=messages
        )
        return completion

    async def generate_text(self, user_input, conversation_history=[]):
        messages = [{"role": "user", "content": user_input}]
        messages = conversation_history + messages
        completion = await self._call_openai(messages)

        # Extract the message content from the completion object
        return completion.choices[0]["message"]["content"]

    def count_tokens_from_messages(
        self, messages
    ):  # gpt-4 and gpt-4-32k are 8192 and 32768 respectively.
        if "gpt-4" in self.model:
            print(
                "Warning: gpt-4 may update over time. Assuming tokenization as per gpt-4-0613."
            )

        num_tokens = 0
        for message in messages:
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
                if key == "name":
                    num_tokens += 1  # Assuming one token for name, adjust as needed
        num_tokens += 3  # every reply is primed with 'assistant'
        return num_tokens

    async def generate_shell_commands(self, action, args=None, options=None):
        instruction = "You are a helpful assistant. You will generate '$SHELL' commands based on user input. Your response should contain **ONLY** the command and **NO explanations or extra characters**."

        messages = [{"role": "system", "content": instruction}]

        function_spec = {
            "name": "generate_shell_command",
            "description": "Generate a shell command based on the provided action and arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The main action or command to execute, e.g., 'ls', 'cd', 'mkdir'.",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "A list of arguments to pass to the command.",
                    },
                    "options": {
                        "type": "object",
                        "description": "Optional flags or options to append to the command.",
                        "properties": {
                            "flag": {"type": "string"},
                            "value": {
                                "type": "string",
                                "description": "Optional value for the flag, if any.",
                            },
                        },
                    },
                },
                "required": ["action"],
            },
        }

        function_call = {"action": function_spec["action"]}

        if args:
            function_call["args"] = function_spec["args"]
        if options:
            function_call["options"] = function_spec["options"]

        messages.append({"role": "user", "content": function_call})

        completion = await asyncio.to_thread(
            openai.ChatCompletion.create, model=self.model, messages=messages
        )

        return completion.choices[0]["message"]["content"]


if __name__ == "__main__":
    chat_gpt = ChatGPT()

    prompt = "Show me how to list all files in the current directory."  # Example prompt
    messages = [{"role": "user", "content": prompt}]

    response = asyncio.run(chat_gpt.generate_text(prompt))
    print(response)

    token_count = chat_gpt.count_tokens_from_messages(messages)
    print(f"Token count for messages: {token_count}")
