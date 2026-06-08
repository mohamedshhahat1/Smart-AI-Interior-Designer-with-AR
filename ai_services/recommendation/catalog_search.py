from typing import Optional

from ai_services.utils.llm_client import get_llm_response_sync, parse_llm_json, is_available


FURNITURE_CATALOG = [
    # --- Sofas & Seating ---
    {"id": "f001", "name": "Modern Blue Sofa", "category": "sofa", "style": "modern", "price": 650, "color": "blue", "material": "fabric", "rating": 4.5, "tags": ["comfortable", "contemporary"]},
    {"id": "f002", "name": "Scandinavian Linen Sofa", "category": "sofa", "style": "scandinavian", "price": 720, "color": "light grey", "material": "linen", "rating": 4.6, "tags": ["minimalist", "soft"]},
    {"id": "f003", "name": "Industrial Leather Sofa", "category": "sofa", "style": "industrial", "price": 980, "color": "brown", "material": "leather", "rating": 4.4, "tags": ["distressed", "loft"]},
    {"id": "f004", "name": "Bohemian Velvet Sofa", "category": "sofa", "style": "bohemian", "price": 850, "color": "teal", "material": "velvet", "rating": 4.7, "tags": ["eclectic", "bold"]},
    {"id": "f005", "name": "Mid-Century Lounge Chair", "category": "chair", "style": "mid_century_modern", "price": 550, "color": "walnut", "material": "leather", "rating": 4.8, "tags": ["iconic", "comfortable"]},
    {"id": "f006", "name": "Modern Accent Chair", "category": "chair", "style": "modern", "price": 320, "color": "charcoal", "material": "fabric", "rating": 4.3, "tags": ["sleek", "compact"]},
    {"id": "f007", "name": "Scandinavian Dining Chair", "category": "chair", "style": "scandinavian", "price": 180, "color": "white", "material": "wood", "rating": 4.5, "tags": ["stackable", "light"]},
    {"id": "f008", "name": "Traditional Wingback Chair", "category": "chair", "style": "traditional", "price": 680, "color": "burgundy", "material": "velvet", "rating": 4.6, "tags": ["classic", "elegant"]},
    {"id": "f009", "name": "Velvet Ottoman", "category": "ottoman", "style": "contemporary", "price": 175, "color": "emerald green", "material": "velvet", "rating": 4.6, "tags": ["seating", "accent"]},
    {"id": "f010", "name": "Rustic Bench", "category": "bench", "style": "rustic", "price": 290, "color": "natural wood", "material": "reclaimed wood", "rating": 4.3, "tags": ["entryway", "farmhouse"]},

    # --- Tables ---
    {"id": "f011", "name": "Scandinavian Oak Coffee Table", "category": "coffee_table", "style": "scandinavian", "price": 280, "color": "natural oak", "material": "wood", "rating": 4.7, "tags": ["minimalist", "light"]},
    {"id": "f012", "name": "Modern Glass Coffee Table", "category": "coffee_table", "style": "modern", "price": 350, "color": "clear", "material": "glass", "rating": 4.4, "tags": ["transparent", "sleek"]},
    {"id": "f013", "name": "Industrial Coffee Table", "category": "coffee_table", "style": "industrial", "price": 310, "color": "black", "material": "iron and wood", "rating": 4.5, "tags": ["raw", "sturdy"]},
    {"id": "f014", "name": "Rustic Dining Table", "category": "table", "style": "rustic", "price": 780, "color": "dark wood", "material": "reclaimed wood", "rating": 4.6, "tags": ["farmhouse", "large"]},
    {"id": "f015", "name": "Modern Dining Table", "category": "table", "style": "modern", "price": 650, "color": "white marble", "material": "marble", "rating": 4.7, "tags": ["elegant", "statement"]},
    {"id": "f016", "name": "Scandinavian Extendable Table", "category": "table", "style": "scandinavian", "price": 520, "color": "birch", "material": "wood", "rating": 4.5, "tags": ["expandable", "practical"]},
    {"id": "f017", "name": "Japanese Low Table", "category": "table", "style": "japanese", "price": 340, "color": "dark walnut", "material": "wood", "rating": 4.4, "tags": ["floor seating", "zen"]},
    {"id": "f018", "name": "Art Deco Side Table", "category": "side_table", "style": "art_deco", "price": 220, "color": "gold and marble", "material": "marble", "rating": 4.6, "tags": ["geometric", "glamorous"]},

    # --- Desks ---
    {"id": "f019", "name": "Minimalist Wood Office Desk", "category": "desk", "style": "minimalist", "price": 420, "color": "white oak", "material": "wood", "rating": 4.6, "tags": ["workspace", "clean"]},
    {"id": "f020", "name": "Industrial Standing Desk", "category": "desk", "style": "industrial", "price": 580, "color": "black", "material": "steel and wood", "rating": 4.5, "tags": ["adjustable", "ergonomic"]},
    {"id": "f021", "name": "Modern L-Shaped Desk", "category": "desk", "style": "modern", "price": 490, "color": "white", "material": "mdf", "rating": 4.3, "tags": ["spacious", "corner"]},
    {"id": "f022", "name": "Traditional Writing Desk", "category": "desk", "style": "traditional", "price": 620, "color": "mahogany", "material": "hardwood", "rating": 4.7, "tags": ["classic", "drawers"]},

    # --- Beds ---
    {"id": "f023", "name": "Japanese Platform Bed Frame", "category": "bed", "style": "japanese", "price": 890, "color": "natural", "material": "bamboo", "rating": 4.5, "tags": ["low profile", "zen"]},
    {"id": "f024", "name": "Modern Upholstered Bed", "category": "bed", "style": "modern", "price": 750, "color": "grey", "material": "fabric", "rating": 4.6, "tags": ["padded headboard", "sleek"]},
    {"id": "f025", "name": "Scandinavian Bed Frame", "category": "bed", "style": "scandinavian", "price": 620, "color": "light wood", "material": "pine", "rating": 4.4, "tags": ["simple", "airy"]},
    {"id": "f026", "name": "Traditional Canopy Bed", "category": "bed", "style": "traditional", "price": 1200, "color": "dark wood", "material": "hardwood", "rating": 4.8, "tags": ["grand", "elegant"]},
    {"id": "f027", "name": "Rustic Barn Wood Bed", "category": "bed", "style": "rustic", "price": 680, "color": "weathered brown", "material": "reclaimed wood", "rating": 4.5, "tags": ["farmhouse", "solid"]},

    # --- Storage ---
    {"id": "f028", "name": "Scandinavian Bookcase", "category": "bookcase", "style": "scandinavian", "price": 320, "color": "white", "material": "wood", "rating": 4.5, "tags": ["storage", "display"]},
    {"id": "f029", "name": "Industrial Metal Bookshelf", "category": "bookcase", "style": "industrial", "price": 280, "color": "black", "material": "iron and wood", "rating": 4.4, "tags": ["open", "loft"]},
    {"id": "f030", "name": "Modern Floating Shelves", "category": "shelf", "style": "modern", "price": 120, "color": "white", "material": "mdf", "rating": 4.3, "tags": ["wall-mounted", "minimalist"]},
    {"id": "f031", "name": "Traditional Nightstand", "category": "nightstand", "style": "traditional", "price": 230, "color": "cherry", "material": "hardwood", "rating": 4.4, "tags": ["bedside", "classic"]},
    {"id": "f032", "name": "Modern Nightstand", "category": "nightstand", "style": "modern", "price": 190, "color": "white", "material": "mdf", "rating": 4.3, "tags": ["compact", "clean lines"]},
    {"id": "f033", "name": "Modern TV Console", "category": "tv_stand", "style": "modern", "price": 380, "color": "matte black", "material": "mdf", "rating": 4.4, "tags": ["media", "storage"]},
    {"id": "f034", "name": "Scandinavian TV Stand", "category": "tv_stand", "style": "scandinavian", "price": 350, "color": "oak", "material": "wood", "rating": 4.5, "tags": ["clean", "retro legs"]},
    {"id": "f035", "name": "Modern Wardrobe", "category": "wardrobe", "style": "modern", "price": 680, "color": "white", "material": "mdf", "rating": 4.4, "tags": ["sliding doors", "spacious"]},
    {"id": "f036", "name": "Rustic Dresser", "category": "dresser", "style": "rustic", "price": 520, "color": "distressed white", "material": "wood", "rating": 4.5, "tags": ["farmhouse", "vintage"]},

    # --- Lighting ---
    {"id": "f037", "name": "Industrial Metal Desk Lamp", "category": "lamp", "style": "industrial", "price": 85, "color": "black", "material": "metal", "rating": 4.3, "tags": ["adjustable", "vintage"]},
    {"id": "f038", "name": "Contemporary Floor Lamp", "category": "lamp", "style": "contemporary", "price": 120, "color": "brass", "material": "metal", "rating": 4.2, "tags": ["arc", "warm light"]},
    {"id": "f039", "name": "Scandinavian Pendant Light", "category": "lamp", "style": "scandinavian", "price": 150, "color": "white", "material": "metal", "rating": 4.6, "tags": ["hanging", "dome"]},
    {"id": "f040", "name": "Modern LED Table Lamp", "category": "lamp", "style": "modern", "price": 95, "color": "matte white", "material": "plastic", "rating": 4.4, "tags": ["dimmable", "usb"]},
    {"id": "f041", "name": "Art Deco Chandelier", "category": "lamp", "style": "art_deco", "price": 450, "color": "gold", "material": "brass and crystal", "rating": 4.8, "tags": ["statement", "luxurious"]},
    {"id": "f042", "name": "Japanese Paper Lantern", "category": "lamp", "style": "japanese", "price": 65, "color": "cream", "material": "rice paper", "rating": 4.3, "tags": ["ambient", "zen"]},
    {"id": "f043", "name": "Farmhouse Lantern Sconce", "category": "lamp", "style": "farmhouse", "price": 75, "color": "black", "material": "iron", "rating": 4.4, "tags": ["wall-mounted", "rustic"]},

    # --- Rugs & Textiles ---
    {"id": "f044", "name": "Bohemian Patterned Rug", "category": "rug", "style": "bohemian", "price": 195, "color": "multicolor", "material": "wool", "rating": 4.4, "tags": ["handwoven", "eclectic"]},
    {"id": "f045", "name": "Modern Geometric Rug", "category": "rug", "style": "modern", "price": 250, "color": "grey and white", "material": "synthetic", "rating": 4.3, "tags": ["easy clean", "bold"]},
    {"id": "f046", "name": "Traditional Persian Rug", "category": "rug", "style": "traditional", "price": 480, "color": "red and blue", "material": "wool", "rating": 4.7, "tags": ["handmade", "ornate"]},
    {"id": "f047", "name": "Scandinavian Sheepskin Rug", "category": "rug", "style": "scandinavian", "price": 90, "color": "white", "material": "sheepskin", "rating": 4.5, "tags": ["cozy", "accent"]},
    {"id": "f048", "name": "Coastal Jute Rug", "category": "rug", "style": "coastal", "price": 160, "color": "natural", "material": "jute", "rating": 4.2, "tags": ["textured", "beach"]},
    {"id": "f049", "name": "Coastal Linen Curtains", "category": "curtain", "style": "coastal", "price": 95, "color": "white", "material": "linen", "rating": 4.3, "tags": ["sheer", "breezy"]},
    {"id": "f050", "name": "Modern Blackout Curtains", "category": "curtain", "style": "modern", "price": 110, "color": "charcoal", "material": "polyester", "rating": 4.4, "tags": ["light blocking", "thermal"]},

    # --- Mirrors & Decor ---
    {"id": "f051", "name": "Art Deco Wall Mirror", "category": "mirror", "style": "art_deco", "price": 210, "color": "gold", "material": "glass", "rating": 4.7, "tags": ["geometric", "glamorous"]},
    {"id": "f052", "name": "Modern Round Mirror", "category": "mirror", "style": "modern", "price": 150, "color": "black frame", "material": "glass", "rating": 4.5, "tags": ["minimalist", "wall"]},
    {"id": "f053", "name": "Bohemian Rattan Mirror", "category": "mirror", "style": "bohemian", "price": 130, "color": "natural", "material": "rattan", "rating": 4.4, "tags": ["woven", "boho"]},
    {"id": "f054", "name": "Mediterranean Terracotta Planter", "category": "planter", "style": "mediterranean", "price": 45, "color": "terracotta", "material": "clay", "rating": 4.3, "tags": ["outdoor", "rustic"]},
    {"id": "f055", "name": "Modern Ceramic Vase", "category": "vase", "style": "modern", "price": 55, "color": "matte white", "material": "ceramic", "rating": 4.5, "tags": ["sculptural", "accent"]},
    {"id": "f056", "name": "Japanese Ikebana Vase", "category": "vase", "style": "japanese", "price": 70, "color": "black", "material": "ceramic", "rating": 4.6, "tags": ["minimal", "artisan"]},

    # --- Kitchen & Dining ---
    {"id": "f057", "name": "Modern Bar Stool", "category": "stool", "style": "modern", "price": 140, "color": "black", "material": "metal and wood", "rating": 4.3, "tags": ["counter height", "swivel"]},
    {"id": "f058", "name": "Industrial Bar Stool", "category": "stool", "style": "industrial", "price": 120, "color": "gunmetal", "material": "metal", "rating": 4.4, "tags": ["stackable", "adjustable"]},
    {"id": "f059", "name": "Farmhouse Buffet Cabinet", "category": "cabinet", "style": "farmhouse", "price": 580, "color": "antique white", "material": "wood", "rating": 4.5, "tags": ["storage", "dining room"]},
    {"id": "f060", "name": "Mediterranean Sideboard", "category": "cabinet", "style": "mediterranean", "price": 720, "color": "dark walnut", "material": "hardwood", "rating": 4.6, "tags": ["carved", "storage"]},

    # --- Budget-Friendly Options ---
    {"id": "f061", "name": "Budget Fabric Sofa", "category": "sofa", "style": "contemporary", "price": 350, "color": "beige", "material": "polyester", "rating": 4.1, "tags": ["affordable", "compact"]},
    {"id": "f062", "name": "Simple Wood Desk", "category": "desk", "style": "minimalist", "price": 150, "color": "pine", "material": "pine wood", "rating": 4.0, "tags": ["budget", "basic"]},
    {"id": "f063", "name": "Basic Bookshelf", "category": "bookcase", "style": "modern", "price": 90, "color": "white", "material": "particle board", "rating": 3.9, "tags": ["affordable", "functional"]},
    {"id": "f064", "name": "Folding Dining Table", "category": "table", "style": "modern", "price": 180, "color": "white", "material": "mdf", "rating": 4.0, "tags": ["space saving", "compact"]},
    {"id": "f065", "name": "Budget Floor Lamp", "category": "lamp", "style": "modern", "price": 40, "color": "black", "material": "metal", "rating": 4.0, "tags": ["simple", "tall"]},
]


class CatalogSearch:
    def __init__(self, catalog: Optional[list[dict]] = None):
        self.catalog = catalog or FURNITURE_CATALOG

    def search(
        self,
        category: Optional[str] = None,
        style: Optional[str] = None,
        max_price: Optional[float] = None,
        color: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        results = list(self.catalog)

        if category:
            results = [item for item in results if item["category"] == category]
        if style:
            results = [
                item for item in results
                if item["style"] == style or style.lower() in " ".join(item.get("tags", []))
            ]
        if max_price:
            results = [item for item in results if item["price"] <= max_price]
        if color:
            results = [
                item for item in results
                if color.lower() in item.get("color", "").lower()
            ]

        results.sort(key=lambda x: x.get("rating", 0), reverse=True)

        if not results and is_available():
            return self._llm_recommend(category, style, max_price, color, limit)

        return results[:limit]

    def _llm_recommend(
        self,
        category: Optional[str],
        style: Optional[str],
        max_price: Optional[float],
        color: Optional[str],
        limit: int,
    ) -> list[dict]:
        constraints = []
        if category:
            constraints.append(f"category: {category}")
        if style:
            constraints.append(f"style: {style}")
        if max_price:
            constraints.append(f"max price: ${max_price:.0f}")
        if color:
            constraints.append(f"color: {color}")

        prompt = (
            f"Suggest {min(limit, 5)} furniture items matching: {', '.join(constraints)}.\n"
            f"Return a JSON array where each item has: name, category, style, price (number), "
            f"color, material, rating (1-5), tags (array of strings)."
        )

        raw = get_llm_response_sync([{"role": "user", "content": prompt}], max_tokens=600)
        data = parse_llm_json(raw)
        if isinstance(data, list):
            results = []
            for i, item in enumerate(data[:limit]):
                if isinstance(item, dict) and item.get("name"):
                    item.setdefault("id", f"llm_{i+1:03d}")
                    item.setdefault("category", category or "furniture")
                    item.setdefault("style", style or "modern")
                    item.setdefault("price", 100)
                    item.setdefault("rating", 4.0)
                    item.setdefault("tags", [])
                    results.append(item)
            return results

        return []

    def get_by_id(self, furniture_id: str) -> Optional[dict]:
        for item in self.catalog:
            if item["id"] == furniture_id:
                return item
        return None

    def get_categories(self) -> list[str]:
        return sorted(set(item["category"] for item in self.catalog))

    def get_styles(self) -> list[str]:
        return sorted(set(item["style"] for item in self.catalog))

    def get_price_range(self, category: Optional[str] = None) -> dict:
        items = self.catalog
        if category:
            items = [item for item in items if item["category"] == category]
        if not items:
            return {"min": 0, "max": 0, "avg": 0}
        prices = [item["price"] for item in items]
        return {"min": min(prices), "max": max(prices), "avg": round(sum(prices) / len(prices), 2)}


catalog_search = CatalogSearch()
