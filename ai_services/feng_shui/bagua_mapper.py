from typing import Optional

from ai_services.utils.llm_client import get_llm_response_sync, is_available


BAGUA_ZONES = {
    "south": {
        "zone": "Fame & Reputation",
        "element": "fire",
        "life_area": "Recognition, reputation, how the world sees you",
        "colors": ["red", "orange", "purple", "pink"],
        "enhancers": ["candles", "triangular shapes", "awards display", "lighting"],
        "avoid": ["water features", "blue/black colors", "mirrors facing out"],
    },
    "southwest": {
        "zone": "Love & Relationships",
        "element": "earth",
        "life_area": "Romantic partnerships, marriage, close relationships",
        "colors": ["pink", "red", "terracotta", "beige"],
        "enhancers": ["paired items", "rose quartz", "romantic art", "fresh flowers"],
        "avoid": ["single images", "work items", "exercise equipment"],
    },
    "west": {
        "zone": "Children & Creativity",
        "element": "metal",
        "life_area": "Creativity, children, joy, new projects",
        "colors": ["white", "metallic", "pastel", "gold"],
        "enhancers": ["art supplies", "whimsical decor", "metal frames", "round shapes"],
        "avoid": ["fire elements", "sharp angular objects"],
    },
    "northwest": {
        "zone": "Helpful People & Travel",
        "element": "metal",
        "life_area": "Mentors, helpful people, travel opportunities",
        "colors": ["grey", "white", "silver", "gold"],
        "enhancers": ["travel photos", "religious/spiritual items", "metal bells"],
        "avoid": ["fire elements", "red colors"],
    },
    "north": {
        "zone": "Career & Life Path",
        "element": "water",
        "life_area": "Career, life purpose, journey through life",
        "colors": ["black", "dark blue", "navy", "charcoal"],
        "enhancers": ["water features", "mirrors", "glass items", "wavy shapes"],
        "avoid": ["earth elements", "large pottery", "heavy furniture blocking flow"],
    },
    "northeast": {
        "zone": "Knowledge & Self-Cultivation",
        "element": "earth",
        "life_area": "Education, wisdom, personal growth, meditation",
        "colors": ["blue", "green", "beige", "sand"],
        "enhancers": ["books", "meditation space", "globe", "mountain imagery"],
        "avoid": ["clutter", "distractions", "electronics"],
    },
    "east": {
        "zone": "Family & Health",
        "element": "wood",
        "life_area": "Family relationships, health, ancestors",
        "colors": ["green", "brown", "teal"],
        "enhancers": ["family photos", "healthy plants", "wooden items", "columnar shapes"],
        "avoid": ["metal objects", "white/metallic excess", "dead plants"],
    },
    "southeast": {
        "zone": "Wealth & Prosperity",
        "element": "wood",
        "life_area": "Financial abundance, prosperity, self-worth",
        "colors": ["purple", "green", "gold", "red"],
        "enhancers": ["healthy plants", "wealth symbols", "flowing water", "abundance bowl"],
        "avoid": ["dead plants", "clutter", "broken items", "trash cans"],
    },
    "center": {
        "zone": "Health & Center",
        "element": "earth",
        "life_area": "Overall wellbeing, grounding, balance",
        "colors": ["yellow", "earth tones", "orange", "brown"],
        "enhancers": ["open space", "earth tones", "ceramic/pottery", "square shapes"],
        "avoid": ["clutter", "heavy furniture", "obstacles to movement"],
    },
}


class BaguaMapper:
    def map_room(
        self,
        room_type: str,
        compass_direction: Optional[str] = None,
        detected_objects: Optional[list[dict]] = None,
        room_dimensions: Optional[dict] = None,
    ) -> list[dict]:
        zones = []

        for direction, zone_data in BAGUA_ZONES.items():
            score = self._evaluate_zone(
                direction, zone_data, room_type, detected_objects, compass_direction
            )

            status = "balanced"
            if score >= 8.0:
                status = "excellent"
            elif score >= 6.0:
                status = "good"
            elif score >= 4.0:
                status = "needs_attention"
            else:
                status = "problematic"

            enhancement = None
            if score < 6.0:
                enhancement = self._suggest_zone_enhancement(
                    direction, zone_data, room_type
                )

            zones.append({
                "zone": zone_data["zone"],
                "direction": direction,
                "element": zone_data["element"],
                "life_area": zone_data["life_area"],
                "colors": zone_data["colors"],
                "status": status,
                "score": round(score, 1),
                "enhancement": enhancement,
            })

        return zones

    def _evaluate_zone(
        self,
        direction: str,
        zone_data: dict,
        room_type: str,
        detected_objects: Optional[list[dict]],
        compass_direction: Optional[str] = None,
    ) -> float:
        score = 5.0

        room_zone_bonuses = {
            "bedroom": {"southwest": 2.0, "west": 1.0},
            "office": {"north": 2.0, "southeast": 1.5, "northeast": 1.0},
            "living_room": {"south": 1.5, "east": 1.5, "center": 1.0},
            "kitchen": {"east": 1.5, "south": 1.0},
            "bathroom": {"north": -1.0},
        }

        bonuses = room_zone_bonuses.get(room_type, {})
        score += bonuses.get(direction, 0)

        if compass_direction and compass_direction.lower() == direction:
            score += 1.5

        if detected_objects:
            element = zone_data["element"]
            for obj in detected_objects:
                label = obj.get("label", "") if isinstance(obj, dict) else str(obj)
                obj_element = self._object_to_element(label)
                if obj_element == element:
                    score += 0.5
                elif self._elements_conflict(obj_element, element):
                    score -= 0.5

        return max(1.0, min(10.0, score))

    def _suggest_zone_enhancement(
        self, direction: str, zone_data: dict, room_type: str
    ) -> str:
        if is_available():
            prompt = (
                f"Give one concise feng shui enhancement tip for the {zone_data['zone']} "
                f"({direction}) zone in a {room_type}. The governing element is {zone_data['element']}. "
                f"Reply with a single actionable sentence, no JSON."
            )
            raw = get_llm_response_sync([{"role": "user", "content": prompt}], max_tokens=100)
            if raw and len(raw.strip()) > 10:
                return raw.strip()

        enhancers = zone_data.get("enhancers", [])
        if enhancers:
            items = ", ".join(enhancers[:2])
            return f"Add {items} to strengthen the {zone_data['zone']} area"
        return f"Enhance the {direction} sector with {zone_data['element']} element items"

    def _object_to_element(self, label: str) -> str:
        element_map = {
            "plant": "wood", "bookshelf": "wood", "desk": "wood",
            "lamp": "fire", "candle": "fire", "tv": "fire",
            "rug": "earth", "ceramic": "earth", "pottery": "earth",
            "mirror": "metal", "clock": "metal", "frame": "metal",
            "fountain": "water", "aquarium": "water", "glass": "water",
        }
        return element_map.get(label.lower(), "earth")

    def _elements_conflict(self, element_a: str, element_b: str) -> bool:
        conflicts = {
            "water": "fire", "fire": "water",
            "fire": "metal", "metal": "fire",
            "metal": "wood", "wood": "metal",
            "wood": "earth", "earth": "wood",
            "earth": "water", "water": "earth",
        }
        return conflicts.get(element_a) == element_b


bagua_mapper = BaguaMapper()
