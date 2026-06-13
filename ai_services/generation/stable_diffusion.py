import os
import torch
from typing import Optional
from PIL import Image

from ai_services.generation.precision import get_inference_dtype, has_limited_vram


class StableDiffusionGenerator:
    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id or os.getenv(
            "STABLE_DIFFUSION_MODEL",
            "stable-diffusion-v1-5/stable-diffusion-v1-5",
        )
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = get_inference_dtype(self.device)

    def load_model(self):
        if self.pipe is not None:
            return
        if self.pipe == "unavailable":
            return

        try:
            from diffusers import StableDiffusionPipeline

            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=self.dtype,
                safety_checker=None,
            )
            if self.dtype == torch.float16:
                # Keep VAE decoding stable while the rest of the pipeline uses FP16.
                self.pipe.vae.register_to_config(force_upcast=True)
            self.pipe.enable_attention_slicing()
            if has_limited_vram(self.device):
                self.pipe.enable_model_cpu_offload()
            else:
                self.pipe = self.pipe.to(self.device)
        except Exception as exc:
            self.pipe = None
            raise RuntimeError("Failed to load the Stable Diffusion 1.5 pipeline") from exc

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
