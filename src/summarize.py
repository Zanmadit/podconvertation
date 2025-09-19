import requests
import json
import re

API_URL = "https://vsjz8fv63q4oju-8000.proxy.runpod.net/v1/chat/completions"
MODEL_NAME = "llama4scout"

def summarize(input_path="data/transcripts/transcript.txt", out_path="data/slides_outline.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print("[INFO] Sending transcript to model...")
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an assistant, you write slide outlines."},
            {"role": "user", "content": f"Break the text into 5–7 slides.\n"
                                        f"Format:\nSlide N:\nTitle: ...\nPoints:\n- ...\n- ...\n\n"
                                        f"Text:\n{transcript}"}
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]

    cleaned = result.lstrip()  
    if cleaned.startswith("Slide"):
        cleaned = cleaned  
    else:
        idx = cleaned.find("Slide")
        if idx != -1:
            cleaned = cleaned[idx:]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned.strip())

    print(f"[INFO] Slides outline saved to {out_path}")
    return cleaned


if __name__ == "__main__":
    summarize()
