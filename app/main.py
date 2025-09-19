import os
import shutil
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data/podcasts"
OUTPUT_DIR = "output"
FRONTEND_DIR = "frontend"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return {"message": "Frontend not found. Please add index.html in frontend/ folder."}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, "podcast.mp3")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print("[INFO] Starting pipeline...")
        subprocess.run(["python", "src/pipeline.py"], check=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"Pipeline failed: {e}"}

    video_path = os.path.join(OUTPUT_DIR, "presentation.mp4")
    pptx_path = os.path.join(OUTPUT_DIR, "presentation.pptx")

    if not os.path.exists(video_path):
        return {"error": "Video not found"}
    if not os.path.exists(pptx_path):
        return {"error": "PPTX not found"}

    return {
        "video": "/output/presentation.mp4",
        "presentation": "/output/presentation.pptx"
    }

