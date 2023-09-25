import openai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# openai.Model.list()


# Use chatGPT's API ($)
async def generate_text(prompt):
    completion = await asyncio.to_thread(
        openai.ChatCompletion.create,
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0]["message"]["content"]


async def generate_shell_commands(prompt):
    completion = await asyncio.to_thread(
        openai.ChatCompletion.create,
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. You will generate '$SHELL' commands based on user input. Your response should contain ONLY the command and NO explanations or extra characters.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0]["message"]["content"]
