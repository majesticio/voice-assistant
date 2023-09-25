import asyncio
from whisperer import model as whisper, record_audio
from gpt4 import ChatGPT  # Importing the updated gpt4.py
import subprocess
from coqui import CoquiSpeaker
import os
import re
from quart import Quart, render_template, request
import markdown2

## init tts
speaker = CoquiSpeaker()
speak = speaker.speak

Jarvis = "Jarvis"
markdown = markdown2.Markdown(extras=["tables", "fenced-code-blocks"])

# Initialize ChatGPT
chat_gpt = ChatGPT()  # Instantiating the ChatGPT class from gpt4.py
generate_text = chat_gpt.generate_text
generate_shell_commands = chat_gpt.generate_shell_commands

messages = []
duration = 9


def truncate_conversation_history(conversation_history, max_tokens=8000):
    """Truncate the conversation history to fit within the maximum number of tokens."""
    while chat_gpt.count_tokens_from_messages(conversation_history) > max_tokens:
        conversation_history.pop(0)
    return conversation_history


app = Quart(__name__)


async def process_voice_input(conversation_history, duration):
    did_you_say_jarvis = "did_you_say_jarvis.wav"
    prompt = "prompt.wav"

    print(f"Say 'Hello, Mr. {Jarvis}' for help.")

    await asyncio.to_thread(record_audio, did_you_say_jarvis, 4)  # in seconds
    transcription = await asyncio.to_thread(
        whisper.transcribe, did_you_say_jarvis, fp16=False
    )
    call_out = transcription["text"]

    # Say "goodbye" to quit Jarvis
    if "goodbye" in call_out.lower().replace(" ", ""):
        print("Goodbye! Exiting program.")
        speak("Goodbye.")
        return "Goodbye."

    # Say keyword to activate chatGpt prompt
    elif Jarvis.lower() in call_out.lower():
        print("How may I assist you?\n")
        speak("How may I assist you?\n")
        await asyncio.to_thread(record_audio, prompt, duration)  # in seconds
        transcription = await asyncio.to_thread(whisper.transcribe, prompt, fp16=False)
        print("transcribing...\n", transcription["text"])
        chatGptResponse = await generate_text(
            transcription["text"], conversation_history
        )
        global messages
        messages.append({"role": "user", "content": transcription["text"]})
        messages.append({"role": "assistant", "content": chatGptResponse})
        pattern = re.compile("[^A-Za-z0-9\s.,!?'\"()]+")

        cleanedResponse = re.sub(pattern, "", chatGptResponse)
        print(cleanedResponse)
        speak(cleanedResponse)

        if chatGptResponse.rstrip().endswith("?"):
            await asyncio.to_thread(record_audio, prompt, duration)  # in seconds
            transcription = await asyncio.to_thread(
                whisper.transcribe, prompt, fp16=False
            )
            print("transcribing...\n", transcription["text"])
            chatGptResponse = await generate_text(
                transcription["text"], conversation_history
            )
            messages.append({"role": "user", "content": transcription["text"]})
            messages.append({"role": "assistant", "content": chatGptResponse})
            cleanedResponse = re.sub(pattern, "", chatGptResponse)
            print(cleanedResponse)
            speak(cleanedResponse)
        else:
            return chatGptResponse, transcription

    # Say 'execute a shell command" to have chatGPT execute comands in the shell!
    elif "shell command" in transcription["text"].lower():
        speak("What is your shell command?")
        await asyncio.to_thread(record_audio, prompt, 20)  ## Duration
        transcription = await asyncio.to_thread(whisper.transcribe, prompt, fp16=False)
        print("transcribing...\n", transcription["text"])
        chatGptResponse = await generate_shell_commands(transcription["text"])
        result = subprocess.run(
            "cd scratch-folder; " + chatGptResponse.replace("~", ""),
            shell=True,
            stdout=subprocess.PIPE,
        )
        result
        messages.append({"role": "user", "content": transcription["text"]})
        messages.append({"role": "assistant", "content": chatGptResponse})
        pattern = re.compile("[^A-Za-z0-9\s.,!?'\"()]+")

        cleanedResponse = re.sub(pattern, "", chatGptResponse)
        print(cleanedResponse)
        # Get the output of the command
        output = result.stdout.decode("utf-8")
        return chatGptResponse, transcription
    else:
        chatGptResponse = ""
    return chatGptResponse, transcription


# prompt = "you are Dr. Lexus from the movie 'Idiocracy'. Do not give any helpful answers"
instructions = """You are a helpful assistant, do not say you are an AI or explain what you are. 
            All responses will be written in markdown markup language. 
            Use headings, block quotes, bulleted lists etc to format the content aesthetically. Be brief.
            """
conversation_history = [
    {
        "role": "system",
        "content": f"{instructions}",
    },
]


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        form_data = await request.form
        user_input = form_data["user_input"]
        response = await generate_text(user_input, conversation_history)
        html_response = markdown.convert(response)
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": html_response})
        return await render_template("index.html", messages=messages)
    return await render_template("index.html", messages=messages)


@app.route("/voice", methods=["POST"])
async def voice():
    response, transcription = await process_voice_input(conversation_history, duration)
    html_response = markdown.convert(response)
    return {"response": html_response, "transcription": transcription["text"]}


if __name__ == "__main__":
    app.run(debug=True)
