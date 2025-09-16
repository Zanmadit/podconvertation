from transcribe import transcribe
from summarize import summarize
from generate_images import generate_images
from generate_pptx import generate_pptx
from make_video import make_video

def main():
    print("[PIPELINE] Step 1: Transcription")
    transcribe()

    print("[PIPELINE] Step 2: Summarization (shai.pro)")
    summarize()

    print("[PIPELINE] Step 3: Image Generation")
    generate_images()

    print("[PIPELINE] Step 4: Presentation Assembly")
    generate_pptx()

    print("[PIPELINE] Step 5: Presentation done")
    make_video()

    print("[PIPELINE] All done!")
    
if __name__ == "__main__":
    main()
