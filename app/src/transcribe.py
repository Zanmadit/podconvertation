from faster_whisper import WhisperModel
from pathlib import Path
import sys

def transcribe(audio_path="data/podcasts/podcast.mp3", out_path="data/transcripts/transcript.txt"):
    print("[INFO] Starting transcription...")
    
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(audio_path)

    transcript = " ".join([seg.text for seg in segments])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("[INFO] Saved transcript to", out_path)


audio_path = sys.argv[1] if len(sys.argv) > 1 else "data/podcasts/podcast.mp3"
transcribe(audio_path)