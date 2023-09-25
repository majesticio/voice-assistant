import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play

# MODEL_NAME="tts_models/en/jenny/jenny"
MODEL_NAME = "tts_models/en/vctk/vits"


class CoquiSpeaker:
    def __init__(self, model_name=MODEL_NAME):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_engine = TTS(model_name=model_name, progress_bar=False).to(device)

    # def speak(self, text, out_path="sounds/jarvis.wav"):
    #     # Synthesize the speech and save to a file
    #     self.tts_engine.tts_to_file(text=text, file_path=out_path)

    #     # Load and play the audio
    #     audio = AudioSegment.from_wav(out_path)
    #     play(audio)
    def speak(self, text, out_path="sounds/jarvis.wav", speaker="p230"):
        # Synthesize the speech and save to a file
        self.tts_engine.tts_to_file(text=text, file_path=out_path, speaker=speaker)

        # Load and play the audio
        audio = AudioSegment.from_wav(out_path)
        play(audio)
