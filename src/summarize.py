import requests
import json

API_URL = "https://bkwg3037dnb7aq-8000.proxy.runpod.net/v1/chat/completions"
MODEL_NAME = "llama4scout"

def summarize(input_path="data/transcripts/transcript.txt", out_path="data/slides_outline.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print("[INFO] Sending transcript to shai.pro...")
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an assistant, you write resumes."},
            {"role": "user", "content": f"Break the text into 5–7 slides.\nFormat:\nTitle: ...\nPoints:\n- ...\n- ...\n\nText:\n{transcript}"}
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"[INFO] Slides outline saved to {out_path}")
    return result

if __name__ == "__main__":
    summarize()
