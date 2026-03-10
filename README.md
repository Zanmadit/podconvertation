# Podconvertation

An application capable of generating a presentation/video presentation from an audio file. Whatever it may be - a university lecture, podcast, and much more.

Pipeline:
Audio -> Whisper transcription -> LLM summarization -> slide images -> PPTX -> (voice) -> video.

Ollama is used, so you need to download it and the model.

## Instructions for use are provided below.

1. Create `.env` by way of `.env.example`

2. Start virtual environment
```
uv venv
source .venv/bin/activate
uv sync
```

3. Run FastAPI:
```
uvicorn app.main:app --reload --port 8000
```

4. Then open index.html in browser.


## Project Structure
```
.
├── app
│   ├── config.py
│   ├── index.html
│   ├── main.py
│   ├── pipeline.py
│   └── src
│       ├── generate_images.py
│       ├── generate_pptx.py
│       ├── make_video.py
│       ├── summarize.py
│       └── transcribe.py
├── data
│   ├── podcasts
│   ├── slides_outline.txt
│   └── transcripts
├── frontend
├── LICENSE
├── output
│   ├── audio
│   ├── images
│   ├── presentation.mp4
│   ├── presentation.pptx
│   └── slides_png
├── pyproject.toml
├── README.md
└── uv.lock
```

Sample files are included in the `data/` directory for testing and demonstration purposes.
An MP3 file of an excerpt from the Lex Fridman with Guido Van Rossum podcast has been provided. [video](https://youtu.be/F2Mx-u7auUs?si=cHiRZ4nmOtuR8OqH)
