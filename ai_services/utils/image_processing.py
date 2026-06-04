import io
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def load_image(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")


def resize_image(
    image: Image.Image,
    max_dimension: int = 1024,
    maintain_aspect: bool = True,
) -> Image.Image:
    if maintain_aspect:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        return image
    return image.resize((max_dimension, max_dimension), Image.Resampling.LANCZOS)


def image_to_bytes(image: Image.Image, format: str = "JPEG", quality: int = 90) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=format, quality=quality)
    return buffer.getvalue()


def bytes_to_image(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data)).convert("RGB")


def enhance_image(
    image: Image.Image,
    brightness: float = 1.0,
    contrast: float = 1.0,
    sharpness: float = 1.0,
    color: float = 1.0,
) -> Image.Image:
    if brightness != 1.0:
        image = ImageEnhance.Brightness(image).enhance(brightness)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if sharpness != 1.0:
        image = ImageEnhance.Sharpness(image).enhance(sharpness)
    if color != 1.0:
        image = ImageEnhance.Color(image).enhance(color)
    return image


def create_thumbnail(
    image: Image.Image, size: tuple[int, int] = (256, 256)
) -> Image.Image:
    thumb = image.copy()
    thumb.thumbnail(size, Image.Resampling.LANCZOS)
    return thumb


def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> list[str]:
    small = image.resize((100, 100), Image.Resampling.LANCZOS)
    pixels = np.array(small).reshape(-1, 3)

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    colors = []
    for center in kmeans.cluster_centers_:
        r, g, b = int(center[0]), int(center[1]), int(center[2])
        colors.append(f"#{r:02x}{g:02x}{b:02x}")

    return colors


def blend_images(
    original: Image.Image,
    generated: Image.Image,
    alpha: float = 0.5,
) -> Image.Image:
    if original.size != generated.size:
        generated = generated.resize(original.size, Image.Resampling.LANCZOS)
    return Image.blend(original, generated, alpha)
