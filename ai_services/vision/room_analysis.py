import os
import tempfile
from typing import Optional
from urllib.parse import urlparse

import httpx

from ai_services.vision.object_detection import detector
from ai_services.vision.segmentation import segmenter


ROOM_TYPE_INDICATORS = {
    "living_room": ["couch", "sofa", "tv", "coffee_table"],
    "bedroom": ["bed", "nightstand", "wardrobe"],
    "kitchen": ["oven", "refrigerator", "sink", "microwave"],
    "bathroom": ["toilet", "sink", "bathtub"],
    "dining_room": ["dining table", "chair"],
    "office": ["desk", "laptop", "monitor", "chair"],
}


def _resolve_image(image_path: str) -> str:
    if os.path.exists(image_path):
        return image_path

    parsed = urlparse(image_path)
    if parsed.scheme in ("http", "https"):
        try:
            response = httpx.get(image_path, timeout=30.0, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise FileNotFoundError(
                f"Failed to download image from {image_path}: HTTP {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise FileNotFoundError(
                f"Cannot reach image storage at {image_path}: {e}"
            ) from e

        ext = os.path.splitext(parsed.path)[-1] or ".jpg"
        tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        tmp.write(response.content)
        tmp.close()
        return tmp.name

    raise FileNotFoundError(f"Image not found and not a valid URL: {image_path}")


class RoomAnalyzer:
    def analyze(self, image_path: str) -> dict:
        local_path = _resolve_image(image_path)
        try:
            detections = detector.detect(local_path)
            segmentation = segmenter.segment_room(local_path)
        finally:
            if local_path != image_path and os.path.exists(local_path):
                os.unlink(local_path)

        room_type = self._classify_room(detections)
        area = self._estimate_area(segmentation)
        objects_summary = detector.get_room_objects_summary(detections)

        return {
            "room_type": room_type,
            "area": area,
            "detected_objects": detections,
            "objects_summary": objects_summary,
            "segmentation_data": segmentation,
        }

    def _classify_room(self, detections: list[dict]) -> str:
        detected_labels = {d["label"].lower() for d in detections}

        best_match = "living_room"
        best_score = 0

        for room_type, indicators in ROOM_TYPE_INDICATORS.items():
            score = sum(1 for ind in indicators if ind in detected_labels)
            if score > best_score:
                best_score = score
                best_match = room_type

        return best_match

    def _estimate_area(self, segmentation: dict) -> Optional[float]:
        floor_data = segmentation.get("floor", {})
        if not floor_data.get("detected"):
            return None

        floor_percentage = floor_data.get("area_percentage", 30)
        dims = segmentation.get("image_dimensions", {})
        width = dims.get("width", 640)
        height = dims.get("height", 480)

        pixel_area = width * height * (floor_percentage / 100)
        estimated_sqm = pixel_area / 10000
        return round(max(8.0, min(estimated_sqm, 100.0)), 1)


room_analyzer = RoomAnalyzer()
