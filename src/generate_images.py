import os
from diffusers import StableDiffusionPipeline
import torch

def generate_images(
    slides_file="data/slides_outline.txt",
    out_dir="output/images",
    style="flat infographic, modern, minimal, pastel colors"
):
    os.makedirs(out_dir, exist_ok=True)

    with open(slides_file, "r", encoding="utf-8") as f:
        slides = f.read().split("Slide")

    print("[INFO] Loading Stable Diffusion v1.5 on GPU...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
    ).to("cuda")

    pipe.safety_checker = None  

    negative_prompt = "blurry, low quality, text, watermark, words, letters, logo"

    for i, slide in enumerate(slides, start=1):
        if slide.strip():
            lines = [line.strip() for line in slide.split("\n") if line.strip()]
            title = [l for l in lines if l.startswith("Title:")]
            points = [l for l in lines if l.startswith("-")]

            title_text = title[0].replace("Title:", "").strip() if title else f"Slide {i}"
            context = ", ".join([p.replace("-", "").strip() for p in points[:2]])

            prompt = f"{style}, digital illustration, {title_text}, no text, no captions, no words"
            negative_prompt = (
                "text, caption, subtitle, title, words, letters, typography, calligraphy, "
                "logo, watermark, signature, poster, meme, screenshot, UI, UX, "
                "book cover, magazine, signboard, billboard"
            )

            image = pipe(
                prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=8
            ).images[0]


            img_path = os.path.join(out_dir, f"slide{i}.png")
            image.save(img_path)

    print(f"[INFO] Images saved in {out_dir}")
