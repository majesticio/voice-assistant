import asyncio
from whisperer import model as whisper, record_audio
from chatGPT import generate_text, generate_shell_commands
import subprocess
from coqui import CoquiSpeaker

## init tts
speaker = CoquiSpeaker()
speak = speaker.speak


# Change the name Jarvis responds to
Jarvis = "Jarvis"

prompt_duration = 16  # How long to record the prompt for chatGPT


async def main(duration):  # in seconds
    """
    pass to record_audio the filename and duration in seconds. the recording
    is transcribed and passed to chatGPT's API and the response is spoken to you with
    text to speech. Fun!
    """
    did_you_say_jarvis = "did_you_say_jarvis.wav"
    prompt = "prompt.wav"
    speak(f"My name is {Jarvis}, hello! How can I help you?\n")

    while True:
        print(f"Say 'Hello, Mr. {Jarvis}' for help.")

        await asyncio.to_thread(record_audio, did_you_say_jarvis, 4)  # in seconds
        transcription = await asyncio.to_thread(
            whisper.transcribe, did_you_say_jarvis, fp16=False
        )

        print("transcribing...\n", transcription["text"], "\n")
        call_out = transcription["text"]

        # Say "goodbye" to quit Jarvis
        if "goodbye" in call_out.lower().replace(" ", ""):
            print("Goodbye! Exiting program.")
            speak("Goodbye.")
            break

        # Say keyword to activate chatGpt prompt
        elif Jarvis.lower() in call_out.lower():
            print("How may I assist you?\n")
            speak("How may I assist you?\n")
            await asyncio.to_thread(record_audio, prompt, duration)  # in seconds
            transcription = await asyncio.to_thread(
                whisper.transcribe, prompt, fp16=False
            )
            print("transcribing...\n", transcription["text"])
            chatGptResponse = await generate_text(transcription["text"])
            print(chatGptResponse, "\n")
            speak(chatGptResponse)

        # Say 'execute a shell command" to have chatGPT execute comands in the shell!
        elif "shell command" in transcription["text"].lower():
            speak("What is your shell command?")
            await asyncio.to_thread(record_audio, prompt, duration)
            transcription = await asyncio.to_thread(
                whisper.transcribe, prompt, fp16=False
            )
            print("transcribing...\n", transcription["text"])
            chatGptResponse = await generate_shell_commands(transcription["text"])
            print(chatGptResponse, "\n")
            subprocess.run(
                chatGptResponse.replace("~", ""),
                shell=True,  # Safety feature NEEDS WORK
            )


if __name__ == "__main__":
    asyncio.run(main(prompt_duration))
