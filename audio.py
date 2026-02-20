import json
import wave
import numpy as np
import soundfile as sf
from vosk import Model, KaldiRecognizer

VOSK_MODEL = "vosk-model-small-ru-0.22"
TARGET_RATE = 16000

_model = Model(VOSK_MODEL)


def convert_ogg_to_wav(ogg_path, wav_path):
    """OGG → WAV, моно 16 kHz (soundfile, без ffmpeg)."""
    data, sr = sf.read(ogg_path)
    if data.ndim == 2:
        data = data.mean(axis=1)
    if sr != TARGET_RATE:
        n = int(len(data) * TARGET_RATE / sr)
        data = np.interp(np.linspace(0, len(data) - 1, n), np.arange(len(data)), data)
    sf.write(wav_path, data, TARGET_RATE)


def wav_to_text(wav_path):
    """Распознавание текста из WAV (офлайн, Vosk)."""
    with wave.open(wav_path, "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getnframes() == 0:
            return ""
        rec = KaldiRecognizer(_model, wav.getframerate())
        parts = []
        while True:
            data = wav.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                part = json.loads(rec.Result()).get("text", "")
                if part:
                    parts.append(part)
        parts.append(json.loads(rec.FinalResult()).get("text", ""))
    return " ".join(filter(None, parts)).strip()
