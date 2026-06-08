import math
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

FURNITURE_COLORS = {
    "sofa": [120, 120, 130, 255], "chair": [160, 120, 80, 255],
    "bed": [200, 190, 180, 255], "desk": [100, 70, 50, 255],
    "table": [160, 120, 80, 255], "coffee_table": [140, 100, 70, 255],
    "tv": [30, 30, 30, 255], "tv_stand": [60, 50, 45, 255],
    "lamp": [180, 160, 100, 255], "bookshelf": [140, 110, 70, 255],
    "wardrobe": [220, 220, 210, 255], "plant": [60, 130, 60, 255],
    "rug": [180, 160, 140, 255], "mirror": [200, 220, 230, 255],
    "curtain": [190, 180, 170, 255],
}

FURNITURE_3D_CATALOG = {
    "sofa": {"width": 2.0, "height": 0.85, "depth": 0.9, "default_model": "models/sofa_modern.glb", "polygon_estimate": 8500},
    "chair": {"width": 0.6, "height": 0.85, "depth": 0.6, "default_model": "models/chair_dining.glb", "polygon_estimate": 4200},
    "bed": {"width": 1.6, "height": 0.6, "depth": 2.0, "default_model": "models/bed_queen.glb", "polygon_estimate": 6800},
    "desk": {"width": 1.2, "height": 0.75, "depth": 0.6, "default_model": "models/desk_office.glb", "polygon_estimate": 3500},
    "table": {"width": 1.0, "height": 0.75, "depth": 1.0, "default_model": "models/table_dining.glb", "polygon_estimate": 3000},
    "coffee_table": {"width": 1.0, "height": 0.45, "depth": 0.6, "default_model": "models/coffee_table.glb", "polygon_estimate": 2500},
    "tv": {"width": 1.2, "height": 0.7, "depth": 0.08, "default_model": "models/tv_flat.glb", "polygon_estimate": 1200},
    "tv_stand": {"width": 1.5, "height": 0.5, "depth": 0.4, "default_model": "models/tv_stand.glb", "polygon_estimate": 3200},
    "lamp": {"width": 0.3, "height": 1.5, "depth": 0.3, "default_model": "models/lamp_floor.glb", "polygon_estimate": 2000},
    "bookshelf": {"width": 0.8, "height": 1.8, "depth": 0.35, "default_model": "models/bookshelf.glb", "polygon_estimate": 5500},
    "wardrobe": {"width": 1.2, "height": 2.0, "depth": 0.6, "default_model": "models/wardrobe.glb", "polygon_estimate": 4000},
    "plant": {"width": 0.4, "height": 0.8, "depth": 0.4, "default_model": "models/plant_pot.glb", "polygon_estimate": 3500},
    "rug": {"width": 2.0, "height": 0.02, "depth": 1.5, "default_model": "models/rug_rect.glb", "polygon_estimate": 500},
    "mirror": {"width": 0.6, "height": 1.0, "depth": 0.05, "default_model": "models/mirror_wall.glb", "polygon_estimate": 800},
    "curtain": {"width": 1.5, "height": 2.4, "depth": 0.1, "default_model": "models/curtain.glb", "polygon_estimate": 2200},
}

QUALITY_SETTINGS = {
    "draft": {"wall_segments": 4, "texture_resolution": 512, "shadow_quality": "none", "polygon_multiplier": 0.3},
    "standard": {"wall_segments": 8, "texture_resolution": 1024, "shadow_quality": "basic", "polygon_multiplier": 1.0},
    "high": {"wall_segments": 16, "texture_resolution": 2048, "shadow_quality": "soft", "polygon_multiplier": 1.5},
    "ultra": {"wall_segments": 32, "texture_resolution": 4096, "shadow_quality": "ray_traced", "polygon_multiplier": 2.5},
}


class MeshGenerator:
    def generate_room_mesh(
        self,
        dimensions: dict,
        quality_level: str = "standard",
    ) -> dict:
        w = dimensions.get("width", 5.0)
        d = dimensions.get("depth", 4.0)
        h = dimensions.get("height", 2.8)
        quality = QUALITY_SETTINGS.get(quality_level, QUALITY_SETTINGS["standard"])

        walls = self._generate_walls(w, d, h, quality["wall_segments"])
        floor = self._generate_floor(w, d)
        ceiling = self._generate_ceiling(w, d, h)

        total_polys = (
            walls["polygon_count"] + floor["polygon_count"] + ceiling["polygon_count"]
        )

        return {
            "geometry": {
                "walls": walls,
                "floor": floor,
                "ceiling": ceiling,
            },
            "dimensions": {"width": w, "depth": d, "height": h},
            "polygon_count": int(total_polys * quality["polygon_multiplier"]),
            "texture_resolution": quality["texture_resolution"],
            "shadow_quality": quality["shadow_quality"],
        }

    def place_furniture(
        self,
        detected_objects: Optional[list[dict]],
        room_dimensions: dict,
    ) -> list[dict]:
        if not detected_objects:
            return []

        w = room_dimensions.get("width", 5.0)
        d = room_dimensions.get("depth", 4.0)
        furniture_objects = []
        placed_positions = []

        for i, obj in enumerate(detected_objects):
            label = (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()
            catalog_entry = FURNITURE_3D_CATALOG.get(label)
            if not catalog_entry:
                continue

            position = self._calculate_placement(
                label, i, len(detected_objects), w, d, placed_positions
            )
            placed_positions.append(position)

            furniture_objects.append({
                "object_id": f"furniture_{i}",
                "name": label.replace("_", " ").title(),
                "category": label,
                "model_url": catalog_entry["default_model"],
                "position": position,
                "rotation": {"x": 0, "y": self._get_rotation(label, position, w, d), "z": 0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
                "dimensions": {
                    "width": catalog_entry["width"],
                    "height": catalog_entry["height"],
                    "depth": catalog_entry["depth"],
                },
                "material": self._get_default_material(label),
                "interactable": True,
                "polygon_count": catalog_entry["polygon_estimate"],
            })

        return furniture_objects

    def generate_lighting(self, room_dimensions: dict, furniture_objects: list[dict]) -> list[dict]:
        w = room_dimensions.get("width", 5.0)
        d = room_dimensions.get("depth", 4.0)
        h = room_dimensions.get("height", 2.8)

        lights = [
            {
                "light_id": "ambient_main",
                "light_type": "ambient",
                "position": {"x": w / 2, "y": h, "z": d / 2},
                "color": "#FFF5E6",
                "intensity": 0.4,
                "cast_shadows": False,
            },
            {
                "light_id": "ceiling_main",
                "light_type": "point",
                "position": {"x": w / 2, "y": h - 0.1, "z": d / 2},
                "color": "#FFFFFF",
                "intensity": 0.8,
                "cast_shadows": True,
            },
            {
                "light_id": "window_light",
                "light_type": "directional",
                "position": {"x": 0, "y": h * 0.7, "z": d / 2},
                "color": "#F0F8FF",
                "intensity": 0.6,
                "cast_shadows": True,
            },
        ]

        for obj in furniture_objects:
            if obj.get("category") == "lamp":
                pos = obj["position"]
                lights.append({
                    "light_id": f"lamp_{obj['object_id']}",
                    "light_type": "point",
                    "position": {"x": pos["x"], "y": pos["y"] + 1.4, "z": pos["z"]},
                    "color": "#FFE4B5",
                    "intensity": 0.5,
                    "cast_shadows": True,
                })

        return lights

    def _generate_walls(self, w: float, d: float, h: float, segments: int) -> dict:
        return {
            "surfaces": [
                {"name": "wall_north", "normal": [0, 0, 1], "vertices": 4 * segments, "position": [w / 2, h / 2, 0]},
                {"name": "wall_south", "normal": [0, 0, -1], "vertices": 4 * segments, "position": [w / 2, h / 2, d]},
                {"name": "wall_east", "normal": [-1, 0, 0], "vertices": 4 * segments, "position": [w, h / 2, d / 2]},
                {"name": "wall_west", "normal": [1, 0, 0], "vertices": 4 * segments, "position": [0, h / 2, d / 2]},
            ],
            "polygon_count": 4 * 2 * segments,
            "material": "wall_paint_matte",
        }

    def _generate_floor(self, w: float, d: float) -> dict:
        return {
            "surface": {"name": "floor", "normal": [0, 1, 0], "position": [w / 2, 0, d / 2]},
            "polygon_count": 2,
            "material": "hardwood_oak",
        }

    def _generate_ceiling(self, w: float, d: float, h: float) -> dict:
        return {
            "surface": {"name": "ceiling", "normal": [0, -1, 0], "position": [w / 2, h, d / 2]},
            "polygon_count": 2,
            "material": "ceiling_white_matte",
        }

    def _calculate_placement(
        self, label: str, index: int, total: int,
        room_width: float, room_depth: float,
        placed: list[dict],
    ) -> dict:
        placements = {
            "sofa": {"x": room_width / 2, "y": 0, "z": room_depth - 1.0},
            "bed": {"x": room_width / 2, "y": 0, "z": room_depth - 1.2},
            "desk": {"x": 0.8, "y": 0, "z": 0.8},
            "tv": {"x": room_width / 2, "y": 0.8, "z": 0.1},
            "tv_stand": {"x": room_width / 2, "y": 0, "z": 0.3},
            "coffee_table": {"x": room_width / 2, "y": 0, "z": room_depth / 2},
            "bookshelf": {"x": room_width - 0.5, "y": 0, "z": room_depth / 2},
            "wardrobe": {"x": 0.4, "y": 0, "z": 0.4},
            "lamp": {"x": room_width - 0.4, "y": 0, "z": room_depth - 0.4},
            "plant": {"x": 0.3, "y": 0, "z": room_depth - 0.3},
        }

        pos = placements.get(label)
        if pos:
            return {k: round(v, 2) for k, v in pos.items()}

        angle = (2 * math.pi * index) / max(total, 1)
        radius = min(room_width, room_depth) * 0.3
        return {
            "x": round(room_width / 2 + radius * math.cos(angle), 2),
            "y": 0,
            "z": round(room_depth / 2 + radius * math.sin(angle), 2),
        }

    def _get_rotation(self, label: str, position: dict, w: float, d: float) -> float:
        if label in ("sofa", "bed"):
            return 0
        if label in ("tv", "mirror"):
            return 180
        if label == "desk":
            return 90 if position["x"] < w / 2 else 270
        return 0

    def _get_default_material(self, label: str) -> str:
        materials = {
            "sofa": "fabric_grey", "chair": "wood_oak", "bed": "fabric_linen",
            "desk": "wood_walnut", "table": "wood_oak", "tv": "plastic_black",
            "lamp": "metal_brass", "bookshelf": "wood_pine", "wardrobe": "wood_white",
            "plant": "ceramic_terracotta", "rug": "wool_cream", "mirror": "glass_clear",
        }
        return materials.get(label, "default_material")

    def export_to_glb(
        self,
        room_geometry: dict,
        furniture_objects: list[dict],
        lighting: list[dict],
        output_path: str,
    ) -> str | None:
        try:
            import trimesh
            import numpy as np
        except ImportError:
            logger.warning("trimesh not installed — cannot export GLB")
            return None

        scene = trimesh.Scene()
        dims = room_geometry.get("dimensions", {"width": 5.0, "depth": 4.0, "height": 2.8})
        w, d, h = dims["width"], dims["depth"], dims["height"]

        floor = trimesh.creation.box(extents=[w, 0.02, d])
        floor.apply_translation([w / 2, -0.01, d / 2])
        floor.visual.face_colors = [180, 150, 110, 255]
        scene.add_geometry(floor, node_name="floor")

        ceiling = trimesh.creation.box(extents=[w, 0.02, d])
        ceiling.apply_translation([w / 2, h + 0.01, d / 2])
        ceiling.visual.face_colors = [245, 245, 240, 255]
        scene.add_geometry(ceiling, node_name="ceiling")

        wall_thickness = 0.08
        walls = [
            ("wall_north", [w, h, wall_thickness], [w / 2, h / 2, wall_thickness / 2]),
            ("wall_south", [w, h, wall_thickness], [w / 2, h / 2, d - wall_thickness / 2]),
            ("wall_east", [wall_thickness, h, d], [w - wall_thickness / 2, h / 2, d / 2]),
            ("wall_west", [wall_thickness, h, d], [wall_thickness / 2, h / 2, d / 2]),
        ]
        for name, extents, translation in walls:
            wall = trimesh.creation.box(extents=extents)
            wall.apply_translation(translation)
            wall.visual.face_colors = [235, 230, 220, 255]
            scene.add_geometry(wall, node_name=name)

        for obj in furniture_objects:
            cat_key = obj.get("category", "")
            cat = FURNITURE_3D_CATALOG.get(cat_key)
            if not cat:
                continue
            fw, fh, fd = cat["width"], cat["height"], cat.get("depth", cat["width"])
            pos = obj.get("position", {"x": 0, "y": 0, "z": 0})

            mesh = trimesh.creation.box(extents=[fw, fh, fd])
            mesh.apply_translation([pos["x"], pos.get("y", 0) + fh / 2, pos["z"]])

            rot = obj.get("rotation", {})
            y_rot = rot.get("y", 0)
            if y_rot:
                angle = math.radians(y_rot)
                rotation_matrix = trimesh.transformations.rotation_matrix(
                    angle, [0, 1, 0], [pos["x"], pos.get("y", 0) + fh / 2, pos["z"]]
                )
                mesh.apply_transform(rotation_matrix)

            color = FURNITURE_COLORS.get(cat_key, [150, 150, 150, 255])
            mesh.visual.face_colors = color
            scene.add_geometry(mesh, node_name=obj.get("object_id", f"furniture_{cat_key}"))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        scene.export(output_path)
        logger.info("Exported GLB to %s", output_path)
        return output_path


mesh_generator = MeshGenerator()
