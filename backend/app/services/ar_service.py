from typing import Optional


class ARService:
    def generate_ar_scene(
        self,
        furniture_list: list[dict],
        room_dimensions: Optional[dict] = None,
    ) -> dict:
        scene_objects = []
        for i, item in enumerate(furniture_list):
            scene_obj = {
                "id": item.get("id", f"obj_{i}"),
                "name": item.get("name", "Unknown"),
                "model_url": item.get("model_3d_url"),
                "position": self._calculate_position(i, len(furniture_list), room_dimensions),
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": self._get_scale(item.get("category", "general")),
                "interactable": True,
            }
            scene_objects.append(scene_obj)

        room_anchor = {
            "type": "plane_detection",
            "alignment": "horizontal",
            "origin": {"x": 0, "y": 0, "z": 0},
        }

        lighting_config = {
            "ambient_intensity": 0.6,
            "directional_light": {
                "direction": {"x": -0.5, "y": -1.0, "z": -0.5},
                "intensity": 0.8,
                "color": "#FFFAF0",
            },
            "shadows_enabled": True,
            "environment_probe": True,
        }

        return {
            "scene_objects": scene_objects,
            "room_anchor": room_anchor,
            "lighting_config": lighting_config,
        }

    def _calculate_position(
        self, index: int, total: int, room_dimensions: Optional[dict]
    ) -> dict:
        if room_dimensions:
            width = room_dimensions.get("width", 5.0)
            depth = room_dimensions.get("depth", 5.0)
            spacing = min(width, depth) / (total + 1)
            return {
                "x": spacing * (index + 1) - width / 2,
                "y": 0,
                "z": spacing * (index + 1) - depth / 2,
            }
        angle_step = 360 / max(total, 1)
        import math
        angle = math.radians(angle_step * index)
        radius = 1.5
        return {
            "x": round(radius * math.cos(angle), 2),
            "y": 0,
            "z": round(radius * math.sin(angle), 2),
        }

    def _get_scale(self, category: str) -> dict:
        scales = {
            "sofa": {"x": 1.0, "y": 1.0, "z": 1.0},
            "chair": {"x": 0.6, "y": 0.6, "z": 0.6},
            "table": {"x": 0.8, "y": 0.8, "z": 0.8},
            "lamp": {"x": 0.4, "y": 0.4, "z": 0.4},
            "bed": {"x": 1.2, "y": 1.0, "z": 1.2},
            "desk": {"x": 0.9, "y": 0.9, "z": 0.9},
            "shelf": {"x": 0.7, "y": 1.0, "z": 0.3},
        }
        return scales.get(category, {"x": 1.0, "y": 1.0, "z": 1.0})


ar_service = ARService()
