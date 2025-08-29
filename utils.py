# utils.py
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

BAD_WORDS = {"idiot", "stupid", "hate", "ugly", "kill"} 


def is_offensive(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in BAD_WORDS)


def maybe_tts(text: str) -> str:
    """Generate audio (mp3) if ENABLE_TTS=true. Returns path or empty string."""
    load_dotenv()
    if os.getenv("ENABLE_TTS", "false").lower() != "true":
        return ""

    client = OpenAI()
    path = "last_recommendation.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text[:4000],
        response_format="mp3",   # ✅ correct param
    ) as response:
        response.stream_to_file(path)

    return path



def maybe_image(prompt_q: str, answer: str) -> str:
    """Generate a book cover image if ENABLE_IMAGE=true."""
    load_dotenv()
    if os.getenv("ENABLE_IMAGE", "false").lower() != "true":
        return ""
    client = OpenAI()

    import re
    m = re.search(r"\*\*(.*?)\*\*|^([A-Z][^\n]+)$", answer)
    title_hint = m.group(1) if m and m.group(1) else "book cover"
    prompt = (
        f"Suggestive book cover for '{title_hint}', inspired by its themes. "
        f"High-quality, printable style."
    )

    img = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")
    b64 = img.data[0].b64_json
    import base64
    png_bytes = base64.b64decode(b64)
    path = "generated_cover.png"
    with open(path, "wb") as f:
        f.write(png_bytes)
    return path
