from typing import Optional


PET_PRODUCTS = {
    "dog": [
        {"name": "Orthopedic Memory Foam Dog Bed", "category": "bedding", "description": "Waterproof, machine-washable cover with supportive memory foam for joint health", "price_range": "$40-$120", "priority": "essential"},
        {"name": "Elevated Stainless Steel Bowls", "category": "feeding", "description": "Adjustable height stand with non-slip base — reduces neck strain", "price_range": "$25-$50", "priority": "essential"},
        {"name": "Pet Water Fountain", "category": "feeding", "description": "Filtered flowing water encourages hydration — dishwasher-safe", "price_range": "$25-$45", "priority": "recommended"},
        {"name": "Heavy-Duty Cord Protector", "category": "safety", "description": "Chew-proof cable covers for all exposed wiring", "price_range": "$15-$30", "priority": "essential"},
        {"name": "Washable Sofa Cover", "category": "furniture_protection", "description": "Waterproof, non-slip sofa protector — machine washable", "price_range": "$30-$60", "priority": "recommended"},
        {"name": "Pet-Safe Stain & Odor Remover", "category": "cleaning", "description": "Enzymatic formula that eliminates odor at molecular level", "price_range": "$10-$20", "priority": "essential"},
        {"name": "Interactive Puzzle Feeder", "category": "enrichment", "description": "Slows eating and provides mental stimulation", "price_range": "$12-$30", "priority": "recommended"},
        {"name": "Pet Camera with Treat Dispenser", "category": "tech", "description": "Monitor and interact with your pet remotely — 2-way audio", "price_range": "$50-$150", "priority": "optional"},
        {"name": "Baby Gate / Pet Gate", "category": "safety", "description": "Pressure-mounted gate to restrict access to certain rooms", "price_range": "$25-$70", "priority": "essential"},
        {"name": "Anti-Scratch Door Protector", "category": "furniture_protection", "description": "Clear acrylic panel shields doors from scratch damage", "price_range": "$15-$30", "priority": "recommended"},
    ],
    "cat": [
        {"name": "Multi-Level Cat Tree", "category": "furniture", "description": "Floor-to-ceiling tree with platforms, sisal posts, and hideaway — essential for vertical space", "price_range": "$60-$200", "priority": "essential"},
        {"name": "Wall-Mounted Cat Shelves", "category": "furniture", "description": "Floating shelves creating an elevated highway around the room", "price_range": "$40-$100", "priority": "recommended"},
        {"name": "Enclosed Self-Cleaning Litter Box", "category": "hygiene", "description": "Automatic rake with carbon filter — reduces odor and daily scooping", "price_range": "$100-$300", "priority": "recommended"},
        {"name": "Sisal Scratching Post (Tall)", "category": "enrichment", "description": "32-inch tall sisal rope post — saves your furniture from claw damage", "price_range": "$20-$50", "priority": "essential"},
        {"name": "Window-Mounted Cat Perch", "category": "enrichment", "description": "Suction-cup perch supporting up to 30 lbs for bird watching", "price_range": "$20-$40", "priority": "recommended"},
        {"name": "Cat Cave Bed", "category": "bedding", "description": "Enclosed felted wool cave providing warmth and security", "price_range": "$30-$60", "priority": "recommended"},
        {"name": "Furniture Scratch Guards", "category": "furniture_protection", "description": "Clear adhesive shields for sofa corners and chair legs", "price_range": "$10-$20", "priority": "essential"},
        {"name": "HEPA Air Purifier", "category": "cleaning", "description": "Captures pet dander, litter dust, and allergens — auto mode adjusts to air quality", "price_range": "$80-$200", "priority": "recommended"},
        {"name": "Interactive Laser Toy", "category": "enrichment", "description": "Automatic random laser pattern for solo play when you're away", "price_range": "$15-$35", "priority": "optional"},
    ],
    "bird": [
        {"name": "Large Flight Cage", "category": "habitat", "description": "Spacious horizontal cage with bar spacing appropriate to species", "price_range": "$80-$300", "priority": "essential"},
        {"name": "Full-Spectrum UV Light", "category": "health", "description": "Simulates natural sunlight for vitamin D synthesis and mood", "price_range": "$25-$60", "priority": "essential"},
        {"name": "Foraging Toys Set", "category": "enrichment", "description": "Shreddable, puzzle, and swing toys to prevent boredom", "price_range": "$15-$30", "priority": "essential"},
        {"name": "Play Gym Stand", "category": "furniture", "description": "Tabletop play area with perches, ladders, and toy hooks for out-of-cage time", "price_range": "$30-$70", "priority": "recommended"},
        {"name": "Bird-Safe Cleaning Spray", "category": "cleaning", "description": "Non-toxic, fragrance-free cage and surface cleaner", "price_range": "$8-$15", "priority": "essential"},
        {"name": "Cage Seed Guard", "category": "cleaning", "description": "Mesh skirt around cage base catches seed hulls and feathers", "price_range": "$12-$25", "priority": "recommended"},
    ],
    "rabbit": [
        {"name": "Large Exercise Pen", "category": "habitat", "description": "Foldable 8-panel pen with door — provides ample hopping space", "price_range": "$35-$70", "priority": "essential"},
        {"name": "Hay Feeder Rack", "category": "feeding", "description": "Wall-mounted hay rack keeps timothy hay clean and accessible", "price_range": "$10-$20", "priority": "essential"},
        {"name": "Cord Protector Tubing", "category": "safety", "description": "Split loom tubing covers all exposed cords from chewing", "price_range": "$10-$15", "priority": "essential"},
        {"name": "Digging Box", "category": "enrichment", "description": "Shallow bin with shredded paper for natural digging behavior", "price_range": "$10-$20", "priority": "recommended"},
        {"name": "Washable Fleece Liner", "category": "bedding", "description": "Soft, absorbent floor cover for enclosure — machine washable", "price_range": "$15-$30", "priority": "recommended"},
    ],
}


class ProductRecommender:
    def recommend(
        self,
        pets: list[dict],
        budget: Optional[float] = None,
        room_type: str = "living_room",
    ) -> list[dict]:
        recommendations = []
        seen = set()

        for pet in pets:
            species = pet.get("species", "dog")
            products = PET_PRODUCTS.get(species, [])

            for product in products:
                if product["name"] in seen:
                    continue
                seen.add(product["name"])

                relevance = self._check_relevance(product, pet, room_type)
                if not relevance:
                    continue

                recommendations.append({
                    "name": product["name"],
                    "category": product["category"],
                    "for_pet_type": species,
                    "description": product["description"],
                    "price_range": product["price_range"],
                    "priority": product["priority"],
                })

        priority_order = {"essential": 0, "recommended": 1, "optional": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 2))

        return recommendations

    def _check_relevance(self, product: dict, pet: dict, room_type: str) -> bool:
        category = product["category"]

        if category == "hygiene" and room_type not in ("bathroom", "utility", "living_room"):
            return False

        if category == "habitat" and room_type == "kitchen":
            return False

        if category == "furniture_protection" and not (pet.get("is_destructive") or pet.get("climbs_furniture")):
            if product["priority"] != "essential":
                return False

        return True


product_recommender = ProductRecommender()
