from typing import Optional


FIVE_ELEMENTS = {
    "wood": {
        "colors": ["green", "brown", "teal"],
        "shapes": ["columnar", "rectangular", "tall"],
        "materials": ["wood", "bamboo", "rattan", "wicker"],
        "season": "spring",
        "direction": "east",
        "yin_yang": "yang",
        "enhancers": ["live plants", "wooden furniture", "floral patterns", "green decor"],
        "produces": "fire",
        "controls": "earth",
        "weakened_by": "metal",
        "destroyed_by": "metal",
    },
    "fire": {
        "colors": ["red", "orange", "purple", "pink", "magenta"],
        "shapes": ["triangular", "pointed", "star"],
        "materials": ["candles", "electronics", "lighting", "leather"],
        "season": "summer",
        "direction": "south",
        "yin_yang": "yang",
        "enhancers": ["candles", "fireplace", "bright lighting", "red accents", "artwork"],
        "produces": "earth",
        "controls": "metal",
        "weakened_by": "water",
        "destroyed_by": "water",
    },
    "earth": {
        "colors": ["yellow", "beige", "terracotta", "sand", "brown"],
        "shapes": ["square", "flat", "horizontal"],
        "materials": ["ceramic", "stone", "brick", "tile", "clay"],
        "season": "late summer",
        "direction": "center",
        "yin_yang": "balance",
        "enhancers": ["crystals", "pottery", "stone sculptures", "landscape art"],
        "produces": "metal",
        "controls": "water",
        "weakened_by": "wood",
        "destroyed_by": "wood",
    },
    "metal": {
        "colors": ["white", "grey", "silver", "gold", "metallic"],
        "shapes": ["round", "oval", "arched", "dome"],
        "materials": ["steel", "iron", "aluminum", "copper", "brass"],
        "season": "autumn",
        "direction": "west",
        "yin_yang": "yin",
        "enhancers": ["metal frames", "wind chimes", "clocks", "round mirrors", "coins"],
        "produces": "water",
        "controls": "wood",
        "weakened_by": "fire",
        "destroyed_by": "fire",
    },
    "water": {
        "colors": ["black", "dark blue", "navy", "charcoal"],
        "shapes": ["wavy", "irregular", "flowing", "asymmetric"],
        "materials": ["glass", "mirror", "water features", "reflective surfaces"],
        "season": "winter",
        "direction": "north",
        "yin_yang": "yin",
        "enhancers": ["fountains", "aquariums", "mirrors", "glass decor", "wavy patterns"],
        "produces": "wood",
        "controls": "fire",
        "weakened_by": "earth",
        "destroyed_by": "earth",
    },
}

ROOM_IDEAL_BALANCE = {
    "living_room": {"wood": 0.20, "fire": 0.20, "earth": 0.25, "metal": 0.15, "water": 0.20},
    "bedroom": {"wood": 0.15, "fire": 0.10, "earth": 0.35, "metal": 0.15, "water": 0.25},
    "office": {"wood": 0.25, "fire": 0.15, "earth": 0.15, "metal": 0.30, "water": 0.15},
    "kitchen": {"wood": 0.15, "fire": 0.30, "earth": 0.25, "metal": 0.20, "water": 0.10},
    "bathroom": {"wood": 0.10, "fire": 0.05, "earth": 0.20, "metal": 0.25, "water": 0.40},
    "dining_room": {"wood": 0.25, "fire": 0.20, "earth": 0.25, "metal": 0.15, "water": 0.15},
}

OBJECT_ELEMENTS = {
    "sofa": "earth", "couch": "earth", "chair": "wood", "bed": "earth",
    "desk": "wood", "table": "wood", "dining table": "wood",
    "tv": "fire", "lamp": "fire", "candle": "fire", "fireplace": "fire",
    "mirror": "water", "fountain": "water", "aquarium": "water", "glass": "water",
    "clock": "metal", "bookshelf": "wood", "plant": "wood",
    "rug": "earth", "curtain": "wood", "painting": "fire",
    "vase": "earth", "sculpture": "metal",
}


class ElementAnalyzer:
    def analyze(
        self,
        room_type: str,
        detected_objects: Optional[list[dict]] = None,
    ) -> list[dict]:
        ideal = ROOM_IDEAL_BALANCE.get(room_type, ROOM_IDEAL_BALANCE["living_room"])
        current = self._detect_current_elements(detected_objects)

        analysis = []
        for element, config in FIVE_ELEMENTS.items():
            current_level = current.get(element, 0.0)
            ideal_level = ideal.get(element, 0.20)

            diff = current_level - ideal_level
            if abs(diff) < 0.05:
                status = "balanced"
            elif diff > 0:
                status = "excess"
            else:
                status = "deficient"

            enhancement_items = []
            if status == "deficient":
                enhancement_items = config["enhancers"][:3]
            elif status == "excess":
                weakener = config["weakened_by"]
                weakener_data = FIVE_ELEMENTS[weakener]
                enhancement_items = [f"Add {weakener} element: {item}" for item in weakener_data["enhancers"][:2]]

            analysis.append({
                "element": element,
                "current_level": round(current_level, 2),
                "ideal_level": round(ideal_level, 2),
                "status": status,
                "associated_colors": config["colors"],
                "associated_shapes": config["shapes"],
                "enhancement_items": enhancement_items,
            })

        return analysis

    def _detect_current_elements(
        self, detected_objects: Optional[list[dict]]
    ) -> dict:
        counts = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}

        if not detected_objects:
            return {k: 0.20 for k in counts}

        for obj in detected_objects:
            label = obj.get("label", "") if isinstance(obj, dict) else str(obj)
            element = OBJECT_ELEMENTS.get(label.lower(), "earth")
            counts[element] += 1

        total = sum(counts.values())
        if total == 0:
            return {k: 0.20 for k in counts}

        return {k: v / total for k, v in counts.items()}

    def get_element_balance_score(self, analysis: list[dict]) -> float:
        total_deviation = 0
        for item in analysis:
            deviation = abs(item["current_level"] - item["ideal_level"])
            total_deviation += deviation

        max_deviation = 2.0
        score = max(1.0, 10.0 - (total_deviation / max_deviation) * 9.0)
        return round(score, 1)

    def calculate_kua_number(self, birth_year: int) -> dict:
        last_two = birth_year % 100
        digit_sum = last_two
        while digit_sum >= 10:
            digit_sum = sum(int(d) for d in str(digit_sum))

        kua = (11 - digit_sum) % 9
        if kua == 0:
            kua = 9

        element_map = {
            1: "water", 2: "earth", 3: "wood", 4: "wood",
            5: "earth", 6: "metal", 7: "metal", 8: "earth", 9: "fire",
        }

        lucky_map = {
            1: ["north", "south", "east", "southeast"],
            2: ["northeast", "west", "northwest", "southwest"],
            3: ["south", "north", "southeast", "east"],
            4: ["north", "south", "east", "southeast"],
            5: ["northeast", "west", "northwest", "southwest"],
            6: ["west", "northeast", "southwest", "northwest"],
            7: ["northwest", "southwest", "northeast", "west"],
            8: ["southwest", "northwest", "west", "northeast"],
            9: ["east", "southeast", "north", "south"],
        }

        unlucky_map = {
            1: ["west", "northeast", "northwest", "southwest"],
            2: ["east", "southeast", "south", "north"],
            3: ["southwest", "northwest", "west", "northeast"],
            4: ["northeast", "west", "northwest", "southwest"],
            5: ["east", "southeast", "south", "north"],
            6: ["south", "north", "southeast", "east"],
            7: ["north", "south", "east", "southeast"],
            8: ["south", "north", "southeast", "east"],
            9: ["northeast", "west", "northwest", "southwest"],
        }

        birth_element = element_map.get(kua, "earth")
        element_data = FIVE_ELEMENTS[birth_element]

        return {
            "kua_number": kua,
            "birth_element": birth_element,
            "lucky_directions": lucky_map.get(kua, []),
            "unlucky_directions": unlucky_map.get(kua, []),
            "compatible_colors": element_data["colors"],
            "compatible_elements": [birth_element, element_data["produces"]],
        }


element_analyzer = ElementAnalyzer()
