import torch
import numpy as np
from typing import Optional
from PIL import Image


class ControlNetPipeline:
    def __init__(self):
        self.pipe = None
        self.controlnet = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        if self.pipe is not None:
            return
        if self.pipe == "unavailable":
            return

        try:
            from diffusers import ControlNetModel, StableDiffusionControlNetPipeline

            self.controlnet = ControlNetModel.from_pretrained(
                "lllyasviel/control_v11p_sd15_canny",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )

            self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "stable-diffusion-v1-5/stable-diffusion-v1-5",
                controlnet=self.controlnet,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
            )
            self.pipe = self.pipe.to(self.device)
        except Exception:
            self.pipe = "unavailable"

    def generate_with_structure(
        self,
        control_image: Image.Image,
        positive_prompt: str,
        negative_prompt: str = "",
        controlnet_conditioning_scale: float = 0.5,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
    ) -> Image.Image:
        self.load_model()

        canny_image = self._extract_edges(control_image)

        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        result = self.pipe(
            prompt=positive_prompt,
            negative_prompt=negative_prompt,
            image=canny_image,
            controlnet_conditioning_scale=controlnet_conditioning_scale,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
        )

        return result.images[0]

    def _extract_edges(self, image: Image.Image) -> Image.Image:
        import cv2

        img_array = np.array(image)

        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        edges = cv2.Canny(gray, 100, 200)
        edges_rgb = np.stack([edges] * 3, axis=-1)

        return Image.fromarray(edges_rgb)

    def redesign_room(
        self,
        original_image: Image.Image,
        prompt_data: dict,
        preserve_strength: float = 0.5,
        seed: Optional[int] = None,
    ) -> Image.Image:
        target_size = (512, 512)
        control_image = original_image.resize(target_size, Image.Resampling.LANCZOS)

        return self.generate_with_structure(
            control_image=control_image,
            positive_prompt=prompt_data["positive"],
            negative_prompt=prompt_data.get("negative", ""),
            controlnet_conditioning_scale=preserve_strength,
            seed=seed,
        )


controlnet_pipeline = ControlNetPipeline()
