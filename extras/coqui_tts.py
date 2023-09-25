import sys
import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Define the model path
MODEL_NAME = "tts_models/en/jenny/jenny"

WAV_PATH = "sounds/jarvis.wav"
# MODEL_NAME = "tts_models/en/ljspeech/fast_pitch"
# MODEL_NAME = "tts_models/en/vctk/vits"
# initialize tts model
tts_engine = TTS(model_name=MODEL_NAME, progress_bar=False).to(device)


def speak(text, out_path=WAV_PATH):
    """
    Synthesize speech from the given text using the specified TTS model.

    Parameters:
    - text (str): The input text to be converted to speech.
    - out_path (str): The path where the output audio will be saved.

    Returns:
    - None
    """
    # Initialize TTS with the model

    # Synthesize the speech and save to a file
    tts_engine.tts_to_file(text=text, file_path=out_path)

    # Load and play the audio
    audio = AudioSegment.from_wav(out_path)
    play(audio)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = "Hello, this is a test for TTS."

    speak(text)
