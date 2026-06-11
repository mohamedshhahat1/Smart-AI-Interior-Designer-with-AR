import os
import numpy as np

from ai_services.utils.image_processing import load_image


class DepthEstimator:
    """Monocular depth estimation for single-image 3D reconstruction."""

    def __init__(self):
        self.model = None
        self.transform = None

    def load_model(self, model_type: str = "DPT_Large"):
        if self.model is not None:
            return
        if os.getenv("ENABLE_MIDAS", "false").lower() not in ("1", "true", "yes"):
            self.model = "heuristic"
            return
        try:
            import torch
            self.model = torch.hub.load("intel-isl/MiDaS", model_type)
            self.model.eval()
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
            if model_type in ("DPT_Large", "DPT_Hybrid"):
                self.transform = midas_transforms.dpt_transform
            else:
                self.transform = midas_transforms.small_transform
        except (ImportError, Exception):
            self.model = "heuristic"

    def estimate_depth(self, image_path: str) -> dict:
        self.load_model()

        image = np.array(load_image(image_path))
        height, width = image.shape[:2]

        if self.model == "heuristic":
            depth_map = self._estimate_depth_from_image(image, height, width)
            method = "heuristic"
        else:
            import torch
            input_batch = self.transform(image)
            with torch.no_grad():
                prediction = self.model(input_batch)
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=(height, width),
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()
            depth_map = prediction.cpu().numpy()
            method = "midas"

        depth_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-8)

        room_dims = self._estimate_room_dimensions(depth_normalized, width, height)

        return {
            "method": method,
            "depth_map": depth_normalized.tolist() if depth_normalized.size < 10000 else None,
            "depth_map_shape": [height, width],
            "min_depth": float(depth_map.min()),
            "max_depth": float(depth_map.max()),
            "mean_depth": float(depth_map.mean()),
            "estimated_dimensions": room_dims,
        }

    def _estimate_depth_from_image(self, image: np.ndarray, height: int, width: int) -> np.ndarray:
        gray = np.mean(image.astype(np.float32), axis=2)

        gray_norm = gray / 255.0

        y_coords = np.linspace(0, 1, height).reshape(-1, 1)
        x_coords = np.linspace(0, 1, width).reshape(1, -1)

        positional_depth = np.where(
            y_coords > 0.65,
            np.clip(1.0 - y_coords * 0.8, 0.2, 1.0) * np.ones((1, width)),
            0.5 + np.abs(x_coords - 0.5) * 0.3,
        )
        positional_depth[:int(height * 0.15), :] = 0.8

        local_var = np.zeros_like(gray_norm)
        k = 16
        for r in range(0, height - k, k):
            for c in range(0, width - k, k):
                patch = gray_norm[r:r+k, c:c+k]
                local_var[r:r+k, c:c+k] = np.var(patch)

        texture_depth = 1.0 - np.clip(local_var * 50, 0, 0.4)

        brightness_depth = 1.0 - gray_norm * 0.3

        depth = positional_depth * 0.5 + texture_depth * 0.25 + brightness_depth * 0.25

        return depth.astype(np.float32)

    def _estimate_room_dimensions(
        self, depth_normalized: np.ndarray, width: int, height: int
    ) -> dict:
        floor_region = depth_normalized[int(height * 0.7):, :]
        wall_region = depth_normalized[int(height * 0.2):int(height * 0.7), :]

        avg_floor_depth = float(np.mean(floor_region))
        avg_wall_depth = float(np.mean(wall_region))

        scale_factor = 8.0
        estimated_depth = avg_floor_depth * scale_factor
        estimated_width = (width / height) * estimated_depth * 1.2
        estimated_height = 2.8

        return {
            "width": round(max(2.5, min(estimated_width, 12.0)), 1),
            "depth": round(max(2.5, min(estimated_depth, 12.0)), 1),
            "height": estimated_height,
            "confidence": round(min(0.85, avg_floor_depth), 2),
        }

    def depth_to_point_cloud(
        self, depth_map: np.ndarray, width: int, height: int,
        focal_length: float = 500.0,
    ) -> list[dict]:
        points = []
        step = max(1, min(width, height) // 100)

        for y in range(0, height, step):
            for x in range(0, width, step):
                z = float(depth_map[y, x])
                if z < 0.01:
                    continue
                px = (x - width / 2) * z / focal_length
                py = (y - height / 2) * z / focal_length
                points.append({"x": round(px, 3), "y": round(-py, 3), "z": round(z, 3)})

        return points


depth_estimator = DepthEstimator()
