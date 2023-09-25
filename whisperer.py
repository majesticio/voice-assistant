import pyaudio
import wave
import whisper

# WHISPER: models include tiny, base, small, medium, and large (lil bit to load)
model = whisper.load_model("base")


def record_audio(filename, seconds):
    """
    Record audio for a specified duration and save it to a WAV file.

    Args:
        filename (str): The name of the WAV file to save the recorded audio to.
        seconds (int): The duration of the recording in seconds.
    """
    print("Listening...\n")
    p = pyaudio.PyAudio()
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    chunk = 1024
    frames = []
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )
    for i in range(0, int(fs / chunk * seconds)):
        # data = stream.read(chunk) # old code
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()
    print("Finished recording.\n")
