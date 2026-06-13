import os
import threading
import torch
import numpy as np
from typing import Optional
from PIL import Image, ImageFilter

from ai_services.generation.precision import get_inference_dtype, has_limited_vram


class ControlNetPipeline:
    def __init__(self):
        self.pipe = None
        self.controlnet = None
        self._inference_lock = threading.Lock()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = get_inference_dtype(self.device)
        self.base_model_id = os.getenv(
            "STABLE_DIFFUSION_INPAINT_MODEL",
            "stable-diffusion-v1-5/stable-diffusion-inpainting",
        )
        self.controlnet_model_id = os.getenv(
            "CONTROLNET_MODEL", "lllyasviel/control_v11p_sd15_canny"
        )

    def load_model(self):
        if self.pipe is not None:
            return
        if self.pipe == "unavailable":
            return

        try:
            from diffusers import (
                ControlNetModel,
                StableDiffusionControlNetInpaintPipeline,
            )

            self.controlnet = ControlNetModel.from_pretrained(
                self.controlnet_model_id,
                torch_dtype=self.dtype,
            )

            pipeline_options = {
                "controlnet": self.controlnet,
                "torch_dtype": self.dtype,
                "safety_checker": None,
            }
            if self.dtype == torch.float16:
                pipeline_options.update(variant="fp16", use_safetensors=True)

            self.pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
                self.base_model_id,
                **pipeline_options,
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
            raise RuntimeError("Failed to load the SD 1.5 ControlNet pipeline") from exc

    def generate_with_structure(
        self,
        original_image: Image.Image,
        positive_prompt: str,
        negative_prompt: str = "",
        mask_image: Optional[Image.Image] = None,
        image_strength: float = 0.9,
        controlnet_conditioning_scale: float = 1.5,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
    ) -> Image.Image:
        with self._inference_lock:
            self.load_model()

            canny_image = self._extract_edges(original_image)
            if mask_image is None:
                mask_image = Image.new("L", original_image.size, color=255)

            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)

            result = self.pipe(
                prompt=positive_prompt,
                negative_prompt=negative_prompt,
                image=original_image,
                mask_image=mask_image,
                control_image=canny_image,
                strength=image_strength,
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
        preserve_strength: Optional[float] = None,
        image_strength: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> Image.Image:
        prepared_image = self._resize_for_generation(original_image)

        layout_prompt = (
            "same room and camera, unchanged walls, floor, ceiling, doors and windows, "
        )
        layout_negative = (
            "different room, changed camera, altered architecture, extra or missing doors "
            "or windows, warped walls, empty room, unfurnished room, "
        )

        is_empty_room = prompt_data.get("is_empty_room", False)
        if image_strength is None:
            image_strength = 1.0 if is_empty_room else 0.72
        if preserve_strength is None:
            preserve_strength = 0.75 if is_empty_room else 1.2
        mask_image = self._create_furnishing_mask(prepared_image) if is_empty_room else None

        return self.generate_with_structure(
            original_image=prepared_image,
            positive_prompt=layout_prompt + prompt_data["positive"],
            negative_prompt=layout_negative + prompt_data.get("negative", ""),
            mask_image=mask_image,
            image_strength=image_strength,
            controlnet_conditioning_scale=preserve_strength,
            seed=seed,
        )

    @staticmethod
    def _resize_for_generation(
        image: Image.Image,
        max_dimension: int = 512,
    ) -> Image.Image:
        width, height = image.size
        scale = max_dimension / max(width, height)
        target_width = max(64, round(width * scale / 8) * 8)
        target_height = max(64, round(height * scale / 8) * 8)
        return image.convert("RGB").resize(
            (target_width, target_height),
            Image.Resampling.LANCZOS,
        )

    @staticmethod
    def _create_furnishing_mask(image: Image.Image) -> Image.Image:
        width, height = image.size
        mask = Image.new("L", (width, height), color=0)
        mask_array = np.array(mask)
        # Keep the upper architecture pixel-stable and only redesign the area
        # where floor-standing furniture can realistically be placed.
        mask_array[int(height * 0.62) :, :] = 255
        return Image.fromarray(mask_array).filter(ImageFilter.GaussianBlur(radius=8))


controlnet_pipeline = ControlNetPipeline()
