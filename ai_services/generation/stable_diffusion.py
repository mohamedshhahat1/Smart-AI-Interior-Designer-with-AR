import os
import torch
import numpy as np
from typing import Optional
from PIL import Image
from pathlib import Path


class StableDiffusionGenerator:
    def __init__(self, model_id: str = "nota-ai/bk-sdm-small"):
        self.model_id = model_id
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        if self.pipe is not None:
            return
        if self.pipe == "unavailable":
            return

        try:
            from diffusers import StableDiffusionPipeline

            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
            )
            self.pipe = self.pipe.to(self.device)
        except Exception:
            self.pipe = "unavailable"

    def generate(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
    ) -> Image.Image:
        self.load_model()

        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        result = self.pipe(
            prompt=positive_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
        )

        return result.images[0]

    def generate_variations(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        num_variations: int = 3,
        **kwargs,
    ) -> list[Image.Image]:
        images = []
        for i in range(num_variations):
            image = self.generate(
                positive_prompt=positive_prompt,
                negative_prompt=negative_prompt,
                seed=42 + i,
                **kwargs,
            )
            images.append(image)
        return images


sdxl_generator = StableDiffusionGenerator()
