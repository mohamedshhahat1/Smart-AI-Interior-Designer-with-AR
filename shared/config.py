"""
Shared configuration constants used across backend and AI services.
"""

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp"]
MAX_IMAGE_SIZE_MB = 20
MAX_IMAGE_DIMENSION = 4096

ROOM_TYPES = [
    "living_room",
    "bedroom",
    "kitchen",
    "bathroom",
    "dining_room",
    "office",
    "studio",
    "hallway",
    "balcony",
]

DESIGN_STYLES = [
    "modern",
    "scandinavian",
    "minimalist",
    "industrial",
    "bohemian",
    "mid_century_modern",
    "contemporary",
    "traditional",
    "rustic",
    "art_deco",
    "japanese",
    "coastal",
    "farmhouse",
    "mediterranean",
]

FURNITURE_CATEGORIES = [
    "sofa",
    "chair",
    "table",
    "desk",
    "bed",
    "wardrobe",
    "shelf",
    "lamp",
    "rug",
    "curtain",
    "mirror",
    "plant",
    "tv_stand",
    "coffee_table",
    "dining_table",
    "nightstand",
    "bookcase",
    "ottoman",
]

DETECTABLE_OBJECTS = [
    "sofa",
    "chair",
    "bed",
    "desk",
    "table",
    "tv",
    "lamp",
    "window",
    "door",
    "plant",
    "bookshelf",
    "wardrobe",
    "rug",
    "mirror",
    "painting",
    "curtain",
]

COST_CATEGORIES = {
    "furniture": "Furniture and major items",
    "decoration": "Paint, wallpaper, curtains, accessories",
    "lighting": "Light fixtures, lamps, smart lighting",
    "flooring": "Floor materials and installation",
    "labor": "Professional installation and assembly",
}

CURRENCY_DEFAULT = "USD"

MINIO_BUCKETS = {
    "room_images": "room-images",
    "generated_designs": "generated-designs",
    "furniture_models": "furniture-models",
    "thumbnails": "thumbnails",
}
