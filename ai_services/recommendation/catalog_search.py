from typing import Optional


SAMPLE_CATALOG = [
    {"id": "f001", "name": "Modern Blue Sofa", "category": "sofa", "style": "modern", "price": 650, "color": "blue", "material": "fabric", "rating": 4.5, "tags": ["comfortable", "contemporary"]},
    {"id": "f002", "name": "Scandinavian Oak Coffee Table", "category": "coffee_table", "style": "scandinavian", "price": 280, "color": "natural oak", "material": "wood", "rating": 4.7, "tags": ["minimalist", "light"]},
    {"id": "f003", "name": "Industrial Metal Desk Lamp", "category": "lamp", "style": "industrial", "price": 85, "color": "black", "material": "metal", "rating": 4.3, "tags": ["adjustable", "vintage"]},
    {"id": "f004", "name": "Minimalist Wood Office Desk", "category": "desk", "style": "minimalist", "price": 420, "color": "white oak", "material": "wood", "rating": 4.6, "tags": ["workspace", "clean"]},
    {"id": "f005", "name": "Bohemian Patterned Rug", "category": "rug", "style": "bohemian", "price": 195, "color": "multicolor", "material": "wool", "rating": 4.4, "tags": ["handwoven", "eclectic"]},
    {"id": "f006", "name": "Mid-Century Lounge Chair", "category": "chair", "style": "mid_century_modern", "price": 550, "color": "walnut", "material": "leather", "rating": 4.8, "tags": ["iconic", "comfortable"]},
    {"id": "f007", "name": "Contemporary Floor Lamp", "category": "lamp", "style": "contemporary", "price": 120, "color": "brass", "material": "metal", "rating": 4.2, "tags": ["arc", "warm light"]},
    {"id": "f008", "name": "Rustic Dining Table", "category": "table", "style": "rustic", "price": 780, "color": "dark wood", "material": "reclaimed wood", "rating": 4.6, "tags": ["farmhouse", "large"]},
    {"id": "f009", "name": "Japanese Platform Bed Frame", "category": "bed", "style": "japanese", "price": 890, "color": "natural", "material": "bamboo", "rating": 4.5, "tags": ["low profile", "zen"]},
    {"id": "f010", "name": "Art Deco Wall Mirror", "category": "mirror", "style": "art_deco", "price": 210, "color": "gold", "material": "glass", "rating": 4.7, "tags": ["geometric", "glamorous"]},
    {"id": "f011", "name": "Coastal Linen Curtains", "category": "curtain", "style": "coastal", "price": 95, "color": "white", "material": "linen", "rating": 4.3, "tags": ["sheer", "breezy"]},
    {"id": "f012", "name": "Modern TV Console", "category": "tv_stand", "style": "modern", "price": 380, "color": "matte black", "material": "mdf", "rating": 4.4, "tags": ["media", "storage"]},
    {"id": "f013", "name": "Scandinavian Bookcase", "category": "bookcase", "style": "scandinavian", "price": 320, "color": "white", "material": "wood", "rating": 4.5, "tags": ["storage", "display"]},
    {"id": "f014", "name": "Velvet Ottoman", "category": "ottoman", "style": "contemporary", "price": 175, "color": "emerald green", "material": "velvet", "rating": 4.6, "tags": ["seating", "accent"]},
    {"id": "f015", "name": "Traditional Nightstand", "category": "nightstand", "style": "traditional", "price": 230, "color": "cherry", "material": "hardwood", "rating": 4.4, "tags": ["bedside", "classic"]},
]


class CatalogSearch:
    def __init__(self, catalog: Optional[list[dict]] = None):
        self.catalog = catalog or SAMPLE_CATALOG

    def search(
        self,
        category: Optional[str] = None,
        style: Optional[str] = None,
        max_price: Optional[float] = None,
        color: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        results = self.catalog

        if category:
            results = [item for item in results if item["category"] == category]
        if style:
            results = [item for item in results if item["style"] == style]
        if max_price:
            results = [item for item in results if item["price"] <= max_price]
        if color:
            results = [
                item for item in results
                if color.lower() in item.get("color", "").lower()
            ]

        results.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return results[:limit]

    def get_by_id(self, furniture_id: str) -> Optional[dict]:
        for item in self.catalog:
            if item["id"] == furniture_id:
                return item
        return None

    def get_categories(self) -> list[str]:
        return list(set(item["category"] for item in self.catalog))

    def get_price_range(self, category: Optional[str] = None) -> dict:
        items = self.catalog
        if category:
            items = [item for item in items if item["category"] == category]
        if not items:
            return {"min": 0, "max": 0}
        prices = [item["price"] for item in items]
        return {"min": min(prices), "max": max(prices), "avg": sum(prices) / len(prices)}


catalog_search = CatalogSearch()
