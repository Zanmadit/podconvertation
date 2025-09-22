import subprocess

def summarize(input_path="data/transcripts/transcript.txt", out_path="data/slides_outline.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print("[INFO] Sending transcript to Ollama (gemma3:4b)...")

    prompt = (
        "You are an assistant, you write slide outlines.\n"
        "Break the text into 5–7 slides.\n"
        "Format:\nSlide N:\nTitle: ...\nPoints:\n- ...\n- ...\n\n"
        f"Text:\n{transcript}"
    )

    result = subprocess.run(
        ["ollama", "run", "gemma3:4b"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )

    output = result.stdout.decode("utf-8").strip()

    cleaned = output.lstrip()
    if not cleaned.startswith("Slide"):
        idx = cleaned.find("Slide")
        if idx != -1:
            cleaned = cleaned[idx:]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned.strip())

    print(f"[INFO] Slides outline saved to {out_path}")
    return cleaned


if __name__ == "__main__":
    summarize()
