import os
import numpy as np
from pathlib import Path
from typing import Optional

from ultralytics import YOLO
from PIL import Image


INTERIOR_LABELS = {
    56: "chair",
    57: "couch",
    58: "potted plant",
    59: "bed",
    60: "dining table",
    62: "tv",
    63: "laptop",
    73: "book",
    74: "clock",
    75: "vase",
}

CUSTOM_LABELS = [
    "sofa", "chair", "bed", "desk", "table", "tv", "lamp",
    "window", "door", "plant", "bookshelf", "wardrobe",
    "rug", "mirror", "painting", "curtain", "coffee_table",
]


class ObjectDetector:
    def __init__(self, model_path: Optional[str] = None):
        if model_path:
            self.model_path = Path(model_path).expanduser()
        else:
            cache_dir = Path(os.getenv("MODEL_CACHE_DIR", "/tmp/models"))
            model_name = os.getenv("YOLO_MODEL", "yolov8x.pt")
            self.model_path = cache_dir / model_name
        self.model = None
        self.confidence_threshold = 0.35

    def load_model(self):
        if self.model is None:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            self.model = YOLO(str(self.model_path))

    def detect(self, image_path: str) -> list[dict]:
        self.load_model()

        results = self.model(image_path, conf=self.confidence_threshold, verbose=False)

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                label = result.names.get(cls_id, f"class_{cls_id}")
                mapped_label = INTERIOR_LABELS.get(cls_id, label)

                detections.append({
                    "label": mapped_label,
                    "confidence": round(confidence, 3),
                    "bounding_box": {
                        "x1": round(xyxy[0], 1),
                        "y1": round(xyxy[1], 1),
                        "x2": round(xyxy[2], 1),
                        "y2": round(xyxy[3], 1),
                    },
                    "class_id": cls_id,
                })

        return sorted(detections, key=lambda x: x["confidence"], reverse=True)

    def detect_from_array(self, image_array: np.ndarray) -> list[dict]:
        self.load_model()
        results = self.model(image_array, conf=self.confidence_threshold, verbose=False)

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                label = result.names.get(cls_id, f"class_{cls_id}")
                mapped_label = INTERIOR_LABELS.get(cls_id, label)

                detections.append({
                    "label": mapped_label,
                    "confidence": round(confidence, 3),
                    "bounding_box": {
                        "x1": round(xyxy[0], 1),
                        "y1": round(xyxy[1], 1),
                        "x2": round(xyxy[2], 1),
                        "y2": round(xyxy[3], 1),
                    },
                })

        return sorted(detections, key=lambda x: x["confidence"], reverse=True)

    def get_room_objects_summary(self, detections: list[dict]) -> dict:
        summary = {}
        for det in detections:
            label = det["label"]
            if label not in summary or det["confidence"] > summary[label]["confidence"]:
                summary[label] = {
                    "count": summary.get(label, {}).get("count", 0) + 1,
                    "confidence": det["confidence"],
                }
            else:
                summary[label]["count"] += 1
        return summary


detector = ObjectDetector()
