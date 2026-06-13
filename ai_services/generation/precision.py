import os

import torch


def get_inference_dtype(device: str) -> torch.dtype:
    if device != "cuda":
        return torch.float32

    precision_setting = os.getenv("AI_FORCE_FULL_PRECISION", "auto").lower()
    if precision_setting in {"1", "true", "yes"}:
        return torch.float32
    if precision_setting in {"0", "false", "no"}:
        return torch.float16

    gpu_name = torch.cuda.get_device_name(0).lower()
    if "gtx 16" in gpu_name:
        return torch.float32
    return torch.float16


def has_limited_vram(device: str) -> bool:
    return device == "cuda" and torch.cuda.get_device_properties(0).total_memory <= 8 * 1024**3
