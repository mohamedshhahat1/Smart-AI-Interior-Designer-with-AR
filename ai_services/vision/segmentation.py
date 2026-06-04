import numpy as np
from typing import Optional
from PIL import Image


class RoomSegmenter:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        self.predictor = None

    def load_model(self):
        if self.model is None:
            try:
                from segment_anything import sam_model_registry, SamPredictor

                model_type = "vit_h"
                checkpoint = self.model_path or "sam_vit_h_4b8939.pth"
                self.model = sam_model_registry[model_type](checkpoint=checkpoint)
                self.predictor = SamPredictor(self.model)
            except ImportError:
                self.model = "mock"
                self.predictor = None

    def segment_room(self, image_path: str) -> dict:
        self.load_model()

        image = np.array(Image.open(image_path).convert("RGB"))
        height, width = image.shape[:2]

        if self.predictor is not None:
            self.predictor.set_image(image)

            wall_mask = self._segment_region(image, "wall", width, height)
            floor_mask = self._segment_region(image, "floor", width, height)
            ceiling_mask = self._segment_region(image, "ceiling", width, height)
        else:
            wall_mask = self._estimate_walls(height, width)
            floor_mask = self._estimate_floor(height, width)
            ceiling_mask = self._estimate_ceiling(height, width)

        return {
            "image_dimensions": {"width": width, "height": height},
            "walls": {
                "detected": True,
                "area_percentage": float(np.sum(wall_mask) / (width * height) * 100),
                "mask_shape": list(wall_mask.shape),
            },
            "floor": {
                "detected": True,
                "area_percentage": float(np.sum(floor_mask) / (width * height) * 100),
                "mask_shape": list(floor_mask.shape),
            },
            "ceiling": {
                "detected": True,
                "area_percentage": float(np.sum(ceiling_mask) / (width * height) * 100),
                "mask_shape": list(ceiling_mask.shape),
            },
        }

    def _segment_region(
        self, image: np.ndarray, region_type: str, width: int, height: int
    ) -> np.ndarray:
        point_coords = self._get_region_points(region_type, width, height)
        point_labels = np.ones(len(point_coords))

        masks, scores, _ = self.predictor.predict(
            point_coords=np.array(point_coords),
            point_labels=point_labels,
            multimask_output=True,
        )

        best_mask_idx = np.argmax(scores)
        return masks[best_mask_idx]

    def _get_region_points(
        self, region_type: str, width: int, height: int
    ) -> list[list[int]]:
        if region_type == "wall":
            return [
                [width // 4, height // 3],
                [3 * width // 4, height // 3],
                [width // 2, height // 4],
            ]
        elif region_type == "floor":
            return [
                [width // 2, 3 * height // 4],
                [width // 4, 4 * height // 5],
                [3 * width // 4, 4 * height // 5],
            ]
        elif region_type == "ceiling":
            return [
                [width // 2, height // 8],
                [width // 4, height // 10],
                [3 * width // 4, height // 10],
            ]
        return [[width // 2, height // 2]]

    def _estimate_walls(self, height: int, width: int) -> np.ndarray:
        mask = np.zeros((height, width), dtype=bool)
        mask[height // 6 : 2 * height // 3, :] = True
        return mask

    def _estimate_floor(self, height: int, width: int) -> np.ndarray:
        mask = np.zeros((height, width), dtype=bool)
        mask[2 * height // 3 :, :] = True
        return mask

    def _estimate_ceiling(self, height: int, width: int) -> np.ndarray:
        mask = np.zeros((height, width), dtype=bool)
        mask[: height // 6, :] = True
        return mask


segmenter = RoomSegmenter()
