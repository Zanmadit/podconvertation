import subprocess
import time
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings


def clean_ollama_output(raw: str) -> str:
    """
    make clean output
    """

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("Slide") or line.startswith("Title:") \
           or line.startswith("Subtitle:") or line.startswith("Points:") \
           or line.startswith("-") or line.startswith("*"):
            line = line.replace("*", "-")
            clean_lines.append(line)
    return "\n".join(clean_lines)


def summarize(input_path="data/transcripts/transcript.txt", out_path="data/slides_outline.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print("[INFO] Starting Ollama server...")
    server_proc = subprocess.Popen([
        "ollama", "serve"
    ])
    time.sleep(5)

    print("[INFO] Sending transcript to Ollama...")
    prompt = (
        "You are an assistant, you write slide outlines.\n"
        "Break the text into 5–7 slides.\n"
        "Format:\nSlide N:\nTitle: ...\nPoints:\n- ...\n- ...\n\n"
        f"Text:\n{transcript}"
    )

    result = subprocess.run(
        ["ollama", "run", settings.LLM_MODEL],
        input=prompt.encode("utf-8"),
        capture_output=True,
        check=True
    )
    output = result.stdout.decode("utf-8").strip()
    cleaned = clean_ollama_output(output)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"[INFO] Slides outline saved to {out_path}")

    print("[INFO] Stopping Ollama server...")
    server_proc.terminate()
    server_proc.wait()
    print("[INFO] Ollama server stopped")

    return cleaned


if __name__ == "__main__":
    summarize()