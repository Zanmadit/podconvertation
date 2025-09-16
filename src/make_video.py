import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def make_video(
    slides_file="data/slides_outline.txt",
    images_dir="output/images",
    out_dir="output",
    lang="en"
):
    os.makedirs(out_dir, exist_ok=True)
    audio_dir = os.path.join(out_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    with open(slides_file, "r", encoding="utf-8") as f:
        slides = f.read().split("Slide")

    clips = []

    for i, slide in enumerate(slides, start=1):
        if not slide.strip():
            continue

        lines = [line.strip() for line in slide.split("\n") if line.strip()]
        title = [l for l in lines if l.startswith("Title:")]
        points = [l for l in lines if l.startswith("-")]

        title_text = title[0].replace("Title:", "").strip() if title else f"Slide {i}"
        context = " ".join([p.replace("-", "").strip() for p in points])

        narration = f"{title_text}. {context}"

        audio_path = os.path.join(audio_dir, f"slide{i}.mp3")
        print(f"[INFO] Generating audio for slide {i}: {title_text}")
        tts = gTTS(text=narration, lang=lang)
        tts.save(audio_path)

        img_path = os.path.join(images_dir, f"slide{i}.png")
        if os.path.exists(img_path):
            audio_clip = AudioFileClip(audio_path)
            clip = ImageClip(img_path).set_duration(audio_clip.duration).set_audio(audio_clip)
            clip = clip.fadein(0.5).fadeout(0.5)
            clips.append(clip)
        else:
            print(f"[WARNING] Image not found for slide {i}: {img_path}")

    if clips:
        final = concatenate_videoclips(clips, method="compose")
        out_path = os.path.join(out_dir, "presentation.mp4")
        final.write_videofile(out_path, fps=24, codec="libx264")
        print(f"[INFO] Video saved to {out_path}")
    else:
        print("[ERROR] No clips to compile. Check your images and slides file.")

if __name__ == "__main__":
    make_video()
