from typing import Optional


CURE_DATABASE = {
    "blocked_pathway": {
        "category": "chi_flow",
        "cures": [
            {"cure": "Remove or reposition furniture blocking natural walking paths", "cost": 0, "element": None, "placement": "pathways"},
            {"cure": "Add a small mirror to visually expand narrow passages", "cost": 25, "element": "water", "placement": "narrow areas"},
            {"cure": "Use round-edged furniture to soften chi flow around obstacles", "cost": 200, "element": "metal", "placement": "pathway intersections"},
        ],
    },
    "overcrowded": {
        "category": "chi_flow",
        "cures": [
            {"cure": "Declutter — remove items that don't serve a purpose or bring joy", "cost": 0, "element": None, "placement": "entire room"},
            {"cure": "Use vertical storage to free floor space for chi circulation", "cost": 150, "element": "wood", "placement": "walls"},
            {"cure": "Replace bulky furniture with sleeker, open-legged alternatives", "cost": 500, "element": "metal", "placement": "main furniture"},
        ],
    },
    "commanding_position": {
        "category": "furniture_placement",
        "cures": [
            {"cure": "Reposition the primary furniture piece to face the door diagonally", "cost": 0, "element": None, "placement": "main seating/bed"},
            {"cure": "If repositioning isn't possible, place a mirror to reflect the doorway", "cost": 30, "element": "water", "placement": "opposite wall"},
        ],
    },
    "mirror_in_bedroom": {
        "category": "bedroom",
        "cures": [
            {"cure": "Cover the mirror at night with a decorative fabric panel", "cost": 20, "element": None, "placement": "over mirror"},
            {"cure": "Relocate the mirror so it does not reflect the bed", "cost": 0, "element": None, "placement": "wall perpendicular to bed"},
            {"cure": "Replace with a smaller mirror angled away from the bed", "cost": 50, "element": "water", "placement": "dresser or closet interior"},
        ],
    },
    "electronics_in_bedroom": {
        "category": "bedroom",
        "cures": [
            {"cure": "Remove or power down electronics 1 hour before sleep", "cost": 0, "element": None, "placement": "bedroom"},
            {"cure": "Place a salt lamp near electronics to absorb electromagnetic energy", "cost": 25, "element": "earth", "placement": "near devices"},
            {"cure": "Use a wooden screen or fabric to separate sleep and work zones", "cost": 80, "element": "wood", "placement": "between bed and electronics"},
        ],
    },
    "fire_water_clash": {
        "category": "kitchen",
        "cures": [
            {"cure": "Place a wooden cutting board or green plant between stove and sink", "cost": 15, "element": "wood", "placement": "between stove and sink"},
            {"cure": "Add a wooden countertop section as a buffer zone", "cost": 200, "element": "wood", "placement": "counter between elements"},
        ],
    },
    "clutter": {
        "category": "energy_flow",
        "cures": [
            {"cure": "Apply the one-year rule — donate or discard items unused for 12 months", "cost": 0, "element": None, "placement": "entire room"},
            {"cure": "Organize remaining items using the Feng Shui 9-box declutter method", "cost": 0, "element": None, "placement": "entire room"},
            {"cure": "Add closed storage solutions to hide visual clutter", "cost": 200, "element": "earth", "placement": "walls and corners"},
            {"cure": "Clear the space under the bed — stored items block restful energy", "cost": 0, "element": None, "placement": "under bed"},
        ],
    },
    "aligned_doors": {
        "category": "chi_flow",
        "cures": [
            {"cure": "Place a tall plant or room divider between aligned doors to slow chi", "cost": 40, "element": "wood", "placement": "between doors"},
            {"cure": "Hang a faceted crystal ball halfway between the doors", "cost": 15, "element": "earth", "placement": "ceiling between doors"},
        ],
    },
    "door_window_alignment": {
        "category": "chi_flow",
        "cures": [
            {"cure": "Place furniture, a plant, or a decorative screen between door and window", "cost": 50, "element": "wood", "placement": "center of room"},
            {"cure": "Add a window treatment (curtain or sheer) to slow escaping chi", "cost": 60, "element": "wood", "placement": "window"},
        ],
    },
    "element_deficiency": {
        "category": "element_balance",
        "cures": {
            "wood": [
                {"cure": "Add live green plants — they are the strongest wood element activator", "cost": 25, "element": "wood", "placement": "east or southeast corner"},
                {"cure": "Incorporate wooden furniture or bamboo accessories", "cost": 100, "element": "wood", "placement": "main areas"},
            ],
            "fire": [
                {"cure": "Add candles, a fireplace feature, or warm-toned lighting", "cost": 30, "element": "fire", "placement": "south area"},
                {"cure": "Hang artwork with warm reds, oranges, or sunset imagery", "cost": 50, "element": "fire", "placement": "south wall"},
            ],
            "earth": [
                {"cure": "Add ceramic pottery, crystals, or stone accessories", "cost": 40, "element": "earth", "placement": "center or southwest"},
                {"cure": "Use earth-tone textiles — terracotta, sand, ochre cushions", "cost": 60, "element": "earth", "placement": "seating areas"},
            ],
            "metal": [
                {"cure": "Add metallic frames, wind chimes, or a round metal mirror", "cost": 35, "element": "metal", "placement": "west or northwest"},
                {"cure": "Include white or metallic accent pieces", "cost": 50, "element": "metal", "placement": "shelves or walls"},
            ],
            "water": [
                {"cure": "Add a small tabletop fountain for gentle water sound", "cost": 45, "element": "water", "placement": "north area"},
                {"cure": "Place mirrors strategically to represent the water element", "cost": 40, "element": "water", "placement": "north wall"},
            ],
        },
    },
}

COLOR_RECOMMENDATIONS = {
    "living_room": {
        "primary": ["warm beige", "soft cream", "light sage green"],
        "accent": ["terracotta", "muted gold", "deep teal"],
        "avoid": ["all-black walls", "harsh neon", "excessive red"],
        "reason": "Balanced warmth promotes gathering and conversation",
    },
    "bedroom": {
        "primary": ["soft white", "pale lavender", "warm blush"],
        "accent": ["dusty rose", "soft grey", "light wood tones"],
        "avoid": ["bright red", "electric blue", "stark black"],
        "reason": "Calming yin colors support rest and intimacy",
    },
    "office": {
        "primary": ["soft grey", "light blue", "warm white"],
        "accent": ["green", "metallic gold", "deep blue"],
        "avoid": ["pure red", "hot pink", "dark heavy colors"],
        "reason": "Mental clarity colors with prosperity accents",
    },
    "kitchen": {
        "primary": ["warm white", "light yellow", "cream"],
        "accent": ["red accents (small)", "green herbs", "copper"],
        "avoid": ["all-blue kitchen", "dark grey", "black cabinets"],
        "reason": "Warm, nourishing colors support the fire element of cooking",
    },
}


class CureRecommender:
    def recommend_cures(
        self,
        chi_flow_issues: list[dict],
        element_analysis: list[dict],
        room_type: str,
    ) -> list[dict]:
        all_cures = []

        for issue in chi_flow_issues:
            issue_type = issue.get("issue_type", "")
            severity = issue.get("severity", "medium")
            cure_data = CURE_DATABASE.get(issue_type)
            if not cure_data:
                continue

            cures_list = cure_data.get("cures", [])
            for i, cure in enumerate(cures_list):
                all_cures.append({
                    "category": cure_data["category"],
                    "severity": severity,
                    "issue_description": issue.get("description", ""),
                    "cure_description": cure["cure"],
                    "element": cure.get("element"),
                    "placement": cure.get("placement"),
                    "estimated_cost": cure.get("cost"),
                    "priority": self._severity_to_priority(severity, i),
                })

        for elem in element_analysis:
            if elem["status"] == "deficient":
                element = elem["element"]
                deficiency_cures = CURE_DATABASE.get("element_deficiency", {}).get("cures", {})
                elem_cures = deficiency_cures.get(element, [])
                for i, cure in enumerate(elem_cures):
                    all_cures.append({
                        "category": "element_balance",
                        "severity": "medium",
                        "issue_description": f"{element.capitalize()} element is deficient (current: {elem['current_level']:.0%}, ideal: {elem['ideal_level']:.0%})",
                        "cure_description": cure["cure"],
                        "element": cure.get("element"),
                        "placement": cure.get("placement"),
                        "estimated_cost": cure.get("cost"),
                        "priority": 3 + i,
                    })

        all_cures.sort(key=lambda x: x["priority"])
        return all_cures

    def get_color_recommendations(self, room_type: str) -> dict:
        return COLOR_RECOMMENDATIONS.get(room_type, COLOR_RECOMMENDATIONS["living_room"])

    def get_furniture_placement_advice(
        self, room_type: str, detected_objects: Optional[list[dict]] = None
    ) -> list[dict]:
        advice = []

        placements = FURNITURE_PLACEMENT_RULES.get(room_type, [])
        detected_labels = set()
        if detected_objects:
            detected_labels = {
                (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()
                for obj in detected_objects
            }

        for rule in placements:
            item = rule["item"]
            is_detected = item.lower() in detected_labels or any(
                item.lower() in label for label in detected_labels
            )
            advice.append({
                "item": item,
                "current_position": "detected" if is_detected else "not detected",
                "recommended_position": rule["position"],
                "reason": rule["reason"],
                "commanding_position": rule.get("commanding", False),
            })

        return advice

    def _severity_to_priority(self, severity: str, index: int) -> int:
        base = {"high": 1, "medium": 3, "low": 5}.get(severity, 3)
        return base + index


FURNITURE_PLACEMENT_RULES = {
    "bedroom": [
        {"item": "Bed", "position": "Against a solid wall, diagonally from the door, not directly in line with it", "reason": "Commanding position for security and restful sleep", "commanding": True},
        {"item": "Nightstand", "position": "Matching pair on both sides of the bed", "reason": "Balance and equality in relationships"},
        {"item": "Mirror", "position": "On a wall perpendicular to the bed, not facing it", "reason": "Prevents disrupted sleep from reflected energy"},
        {"item": "Desk", "position": "As far from the bed as possible, facing the door", "reason": "Separates work energy from rest energy"},
    ],
    "living_room": [
        {"item": "Sofa", "position": "Against a solid wall, facing the main entrance", "reason": "Commanding position provides security and awareness", "commanding": True},
        {"item": "Coffee Table", "position": "Center of seating arrangement with rounded edges preferred", "reason": "Promotes smooth chi flow and prevents sha chi from sharp corners"},
        {"item": "TV", "position": "Not directly opposite the main entrance", "reason": "Prevents chi from being pulled directly out the door"},
        {"item": "Plants", "position": "Corners of the room, especially southeast for wealth", "reason": "Activate stagnant corner energy and bring wood element vitality"},
    ],
    "office": [
        {"item": "Desk", "position": "Facing the door diagonally with a solid wall behind you", "reason": "Commanding position for authority, confidence, and career success", "commanding": True},
        {"item": "Chair", "position": "High-backed chair for support", "reason": "Represents backing and support in your career"},
        {"item": "Bookshelf", "position": "East wall for knowledge, southeast for wealth resources", "reason": "Wood element enhances growth and learning"},
        {"item": "Plant", "position": "Desktop or southeast corner", "reason": "Brings growth energy and absorbs stale air"},
    ],
    "kitchen": [
        {"item": "Stove", "position": "Not directly opposite or adjacent to sink", "reason": "Fire and water elements clash — wood element between them mediates", "commanding": True},
        {"item": "Dining Table", "position": "Center or east side with clear pathways", "reason": "Promotes family togetherness and healthy wood element energy"},
    ],
}


cure_recommender = CureRecommender()
