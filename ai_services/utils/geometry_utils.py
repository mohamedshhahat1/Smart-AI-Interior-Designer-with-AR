import math
from typing import Optional


def calculate_room_area(width: float, depth: float) -> float:
    return round(width * depth, 2)


def calculate_wall_area(
    width: float, depth: float, height: float = 2.8, window_area: float = 0
) -> float:
    perimeter = 2 * (width + depth)
    total_wall = perimeter * height
    return round(total_wall - window_area, 2)


def estimate_room_dimensions_from_image(
    image_width: int,
    image_height: int,
    floor_percentage: float,
    known_object_size: Optional[dict] = None,
) -> dict:
    REFERENCE_SIZES = {
        "door": {"width": 0.9, "height": 2.1},
        "window": {"width": 1.2, "height": 1.0},
        "chair": {"width": 0.5, "height": 0.85},
        "sofa": {"width": 2.0, "height": 0.85},
        "bed": {"width": 1.5, "height": 0.6},
    }

    scale_factor = 0.01
    if known_object_size:
        obj_type = known_object_size.get("type")
        pixel_width = known_object_size.get("pixel_width", 100)
        if obj_type in REFERENCE_SIZES:
            real_width = REFERENCE_SIZES[obj_type]["width"]
            scale_factor = real_width / pixel_width

    estimated_width = round(image_width * scale_factor, 1)
    estimated_depth = round(image_height * scale_factor * (floor_percentage / 100), 1)
    estimated_width = max(2.5, min(estimated_width, 15.0))
    estimated_depth = max(2.5, min(estimated_depth, 15.0))

    return {
        "width": estimated_width,
        "depth": estimated_depth,
        "height": 2.8,
        "area": calculate_room_area(estimated_width, estimated_depth),
    }


def calculate_furniture_position(
    room_width: float,
    room_depth: float,
    furniture_width: float,
    furniture_depth: float,
    placement: str = "center",
) -> dict:
    positions = {
        "center": {
            "x": (room_width - furniture_width) / 2,
            "z": (room_depth - furniture_depth) / 2,
        },
        "wall_left": {
            "x": 0.1,
            "z": (room_depth - furniture_depth) / 2,
        },
        "wall_right": {
            "x": room_width - furniture_width - 0.1,
            "z": (room_depth - furniture_depth) / 2,
        },
        "wall_back": {
            "x": (room_width - furniture_width) / 2,
            "z": 0.1,
        },
        "corner": {
            "x": 0.1,
            "z": 0.1,
        },
    }

    pos = positions.get(placement, positions["center"])
    pos["y"] = 0
    return {k: round(v, 2) for k, v in pos.items()}


def point_in_room(
    x: float, z: float, room_width: float, room_depth: float
) -> bool:
    return 0 <= x <= room_width and 0 <= z <= room_depth


def distance_between_points(
    p1: dict, p2: dict
) -> float:
    dx = p1.get("x", 0) - p2.get("x", 0)
    dy = p1.get("y", 0) - p2.get("y", 0)
    dz = p1.get("z", 0) - p2.get("z", 0)
    return round(math.sqrt(dx * dx + dy * dy + dz * dz), 3)
