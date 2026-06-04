import math
from typing import Optional


class SceneBuilder:
    """Composes complete 3D scenes with camera paths and walkthrough navigation."""

    def build_camera_positions(self, room_dimensions: dict) -> list[dict]:
        w = room_dimensions.get("width", 5.0)
        d = room_dimensions.get("depth", 4.0)
        h = room_dimensions.get("height", 2.8)
        eye_height = 1.6

        return [
            {
                "position_id": "overview",
                "label": "Room Overview",
                "position": {"x": w / 2, "y": h * 0.9, "z": d + 1.0},
                "look_at": {"x": w / 2, "y": 0, "z": d / 2},
                "fov": 75.0,
            },
            {
                "position_id": "entrance",
                "label": "Entrance View",
                "position": {"x": w / 2, "y": eye_height, "z": d - 0.3},
                "look_at": {"x": w / 2, "y": eye_height * 0.7, "z": 0},
                "fov": 60.0,
            },
            {
                "position_id": "center",
                "label": "Center of Room",
                "position": {"x": w / 2, "y": eye_height, "z": d / 2},
                "look_at": {"x": 0, "y": eye_height * 0.7, "z": d / 2},
                "fov": 60.0,
            },
            {
                "position_id": "corner_left",
                "label": "Left Corner",
                "position": {"x": 0.5, "y": eye_height, "z": d - 0.5},
                "look_at": {"x": w, "y": eye_height * 0.5, "z": 0},
                "fov": 65.0,
            },
            {
                "position_id": "corner_right",
                "label": "Right Corner",
                "position": {"x": w - 0.5, "y": eye_height, "z": d - 0.5},
                "look_at": {"x": 0, "y": eye_height * 0.5, "z": 0},
                "fov": 65.0,
            },
            {
                "position_id": "low_angle",
                "label": "Low Angle Detail",
                "position": {"x": w / 2, "y": 0.5, "z": d / 2},
                "look_at": {"x": w / 2, "y": 1.5, "z": 0},
                "fov": 50.0,
            },
        ]

    def build_walkthrough_path(
        self,
        room_dimensions: dict,
        furniture_objects: Optional[list[dict]] = None,
        path_type: str = "tour",
    ) -> list[dict]:
        w = room_dimensions.get("width", 5.0)
        d = room_dimensions.get("depth", 4.0)
        eye = 1.6

        if path_type == "tour":
            return self._build_tour_path(w, d, eye)
        elif path_type == "orbit":
            return self._build_orbit_path(w, d, eye)
        elif path_type == "furniture_focus":
            return self._build_furniture_path(w, d, eye, furniture_objects)
        return self._build_tour_path(w, d, eye)

    def _build_tour_path(self, w: float, d: float, eye: float) -> list[dict]:
        center_x, center_z = w / 2, d / 2
        return [
            {"index": 0, "position": {"x": center_x, "y": eye, "z": d - 0.3}, "look_at": {"x": center_x, "y": eye * 0.7, "z": 0}, "duration_seconds": 3.0, "easing": "ease_in"},
            {"index": 1, "position": {"x": 0.5, "y": eye, "z": d * 0.7}, "look_at": {"x": w, "y": eye * 0.5, "z": d * 0.3}, "duration_seconds": 4.0, "easing": "ease_in_out"},
            {"index": 2, "position": {"x": 0.5, "y": eye, "z": 0.5}, "look_at": {"x": w, "y": eye * 0.5, "z": d}, "duration_seconds": 3.5, "easing": "ease_in_out"},
            {"index": 3, "position": {"x": center_x, "y": eye, "z": 0.5}, "look_at": {"x": center_x, "y": eye * 0.7, "z": d}, "duration_seconds": 3.0, "easing": "ease_in_out"},
            {"index": 4, "position": {"x": w - 0.5, "y": eye, "z": 0.5}, "look_at": {"x": 0, "y": eye * 0.5, "z": d}, "duration_seconds": 3.5, "easing": "ease_in_out"},
            {"index": 5, "position": {"x": w - 0.5, "y": eye, "z": d * 0.7}, "look_at": {"x": 0, "y": eye * 0.5, "z": d * 0.3}, "duration_seconds": 4.0, "easing": "ease_in_out"},
            {"index": 6, "position": {"x": center_x, "y": eye, "z": center_z}, "look_at": {"x": center_x, "y": 0, "z": center_z}, "duration_seconds": 3.0, "easing": "ease_out"},
        ]

    def _build_orbit_path(self, w: float, d: float, eye: float) -> list[dict]:
        center_x, center_z = w / 2, d / 2
        radius = min(w, d) * 0.4
        steps = 12
        path = []

        for i in range(steps + 1):
            angle = (2 * math.pi * i) / steps
            path.append({
                "index": i,
                "position": {
                    "x": round(center_x + radius * math.cos(angle), 2),
                    "y": eye,
                    "z": round(center_z + radius * math.sin(angle), 2),
                },
                "look_at": {"x": center_x, "y": eye * 0.5, "z": center_z},
                "duration_seconds": 2.0,
                "easing": "linear",
            })

        return path

    def _build_furniture_path(
        self, w: float, d: float, eye: float,
        furniture: Optional[list[dict]],
    ) -> list[dict]:
        if not furniture:
            return self._build_tour_path(w, d, eye)

        path = [
            {"index": 0, "position": {"x": w / 2, "y": eye, "z": d - 0.3}, "look_at": {"x": w / 2, "y": eye * 0.7, "z": 0}, "duration_seconds": 2.0, "easing": "ease_in"},
        ]

        for i, obj in enumerate(furniture[:8]):
            pos = obj.get("position", {"x": w / 2, "y": 0, "z": d / 2})
            approach_dist = 1.5
            cam_z = min(d - 0.3, pos.get("z", 0) + approach_dist)

            path.append({
                "index": i + 1,
                "position": {"x": pos.get("x", 0), "y": eye, "z": cam_z},
                "look_at": {"x": pos.get("x", 0), "y": pos.get("y", 0) + 0.5, "z": pos.get("z", 0)},
                "duration_seconds": 3.0,
                "easing": "ease_in_out",
            })

        return path

    def estimate_model_stats(
        self,
        room_geometry: dict,
        furniture_objects: list[dict],
        quality_level: str = "standard",
    ) -> dict:
        room_polys = room_geometry.get("polygon_count", 100)
        furniture_polys = sum(obj.get("polygon_count", 2000) for obj in furniture_objects)
        total_polys = room_polys + furniture_polys

        quality_mult = {"draft": 0.3, "standard": 1.0, "high": 1.5, "ultra": 2.5}.get(quality_level, 1.0)
        total_polys = int(total_polys * quality_mult)

        size_mb = total_polys * 0.00015

        est_seconds = total_polys * 0.001
        if quality_level == "ultra":
            est_seconds *= 3

        return {
            "polygon_count": total_polys,
            "file_size_mb": round(size_mb, 2),
            "estimated_processing_seconds": round(est_seconds, 1),
            "furniture_count": len(furniture_objects),
            "light_count": 3 + sum(1 for f in furniture_objects if f.get("category") == "lamp"),
        }

    def compose_scene(
        self,
        room_geometry: dict,
        furniture_objects: list[dict],
        lighting: list[dict],
        camera_positions: list[dict],
        walkthrough_path: list[dict],
        quality_level: str = "standard",
    ) -> dict:
        stats = self.estimate_model_stats(room_geometry, furniture_objects, quality_level)

        return {
            "scene": {
                "room_geometry": room_geometry,
                "furniture_objects": furniture_objects,
                "lighting": lighting,
                "camera_positions": camera_positions,
                "walkthrough_path": walkthrough_path,
            },
            "metadata": {
                **stats,
                "quality_level": quality_level,
                "output_formats": ["glb", "usdz"],
            },
        }


scene_builder = SceneBuilder()
