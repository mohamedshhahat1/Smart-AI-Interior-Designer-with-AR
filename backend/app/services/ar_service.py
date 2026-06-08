from typing import Optional

_MODEL_BASE = (
    "https://raw.githubusercontent.com/ToxSam/"
    "cc0-models-Polygonal-Mind/main/projects"
)

_FURNITURE_MODELS = {
    "sofa": f"{_MODEL_BASE}/avatar-show/Sofa.glb",
    "couch": f"{_MODEL_BASE}/avatar-show/Sofa.glb",
    "loveseat": f"{_MODEL_BASE}/avatar-show/Sofa.glb",
    "table": f"{_MODEL_BASE}/avatar-show/Table.glb",
    "desk": f"{_MODEL_BASE}/avatar-show/Table.glb",
    "coffee table": f"{_MODEL_BASE}/avatar-show/Table_Round_01.glb",
    "dining table": f"{_MODEL_BASE}/avatar-show/Table_Futuristic.glb",
    "lamp": f"{_MODEL_BASE}/avatar-show/Lamp_Stand.glb",
    "light": f"{_MODEL_BASE}/avatar-show/Lamp_Stand.glb",
    "table lamp": f"{_MODEL_BASE}/avatar-show/TableLamp.glb",
    "wall lamp": f"{_MODEL_BASE}/avatar-show/Lamp_Wall.glb",
    "chair": f"{_MODEL_BASE}/avatar-show/Arm_Chair.glb",
    "armchair": f"{_MODEL_BASE}/avatar-show/Arm_Chair.glb",
    "lounge": f"{_MODEL_BASE}/avatar-show/Long_Chair.glb",
    "bookshelf": f"{_MODEL_BASE}/ca-world/Shelf_01_a.glb",
    "shelf": f"{_MODEL_BASE}/ca-world/Shelf_01_a.glb",
    "cabinet": f"{_MODEL_BASE}/ca-world/Shelf_01_a.glb",
    "plant": f"{_MODEL_BASE}/avatar-show/Banana_Plant.glb",
    "flower": f"{_MODEL_BASE}/avatar-show/Pot_Plant.glb",
    "pot": f"{_MODEL_BASE}/avatar-show/Pot_Plant.glb",
    "carpet": f"{_MODEL_BASE}/avatar-show/Carpet.glb",
    "rug": f"{_MODEL_BASE}/avatar-show/Carpet.glb",
    "bench": f"{_MODEL_BASE}/ca-world/Bench_01.glb",
    "stool": f"{_MODEL_BASE}/ca-world/Stool_01.glb",
}

_DEFAULT_MODEL = f"{_MODEL_BASE}/avatar-show/Arm_Chair.glb"


def _resolve_model_url(name: str) -> str:
    lower = name.lower()
    for keyword, url in _FURNITURE_MODELS.items():
        if keyword in lower:
            return url
    return _DEFAULT_MODEL


class ARService:
    def generate_ar_scene(
        self,
        furniture_list: list[dict],
        room_dimensions: Optional[dict] = None,
    ) -> dict:
        scene_objects = []
        for i, item in enumerate(furniture_list):
            explicit_url = item.get("model_3d_url")
            model_url = (
                explicit_url
                if explicit_url and "Astronaut" not in explicit_url
                else _resolve_model_url(item.get("name", ""))
            )
            scene_obj = {
                "id": item.get("id", f"obj_{i}"),
                "name": item.get("name", "Unknown"),
                "model_url": model_url,
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
            "couch": {"x": 1.0, "y": 1.0, "z": 1.0},
            "chair": {"x": 0.6, "y": 0.6, "z": 0.6},
            "armchair": {"x": 0.7, "y": 0.7, "z": 0.7},
            "table": {"x": 0.8, "y": 0.8, "z": 0.8},
            "lamp": {"x": 0.4, "y": 0.4, "z": 0.4},
            "bed": {"x": 1.2, "y": 1.0, "z": 1.2},
            "desk": {"x": 0.9, "y": 0.9, "z": 0.9},
            "shelf": {"x": 0.7, "y": 1.0, "z": 0.3},
            "bookshelf": {"x": 0.7, "y": 1.0, "z": 0.3},
            "cabinet": {"x": 0.7, "y": 1.0, "z": 0.4},
            "plant": {"x": 0.3, "y": 0.3, "z": 0.3},
            "carpet": {"x": 1.5, "y": 0.05, "z": 1.5},
            "rug": {"x": 1.5, "y": 0.05, "z": 1.5},
            "bench": {"x": 0.8, "y": 0.8, "z": 0.8},
            "stool": {"x": 0.4, "y": 0.4, "z": 0.4},
        }
        return scales.get(category.lower(), {"x": 1.0, "y": 1.0, "z": 1.0})


ar_service = ARService()
