from typing import Optional

from ai_services.utils.llm_client import get_llm_response_sync, parse_llm_json, is_available


TOXIC_PLANTS = {
    "lilies": {"toxic_to": ["cat"], "severity": "critical", "effect": "Kidney failure — even small amounts are lethal to cats"},
    "sago_palm": {"toxic_to": ["dog", "cat"], "severity": "critical", "effect": "Liver failure, potentially fatal"},
    "pothos": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Oral irritation, vomiting, difficulty swallowing"},
    "philodendron": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Oral burning, swelling, drooling"},
    "aloe_vera": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Vomiting, diarrhea, lethargy"},
    "dieffenbachia": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Intense oral irritation, tongue swelling"},
    "oleander": {"toxic_to": ["dog", "cat", "bird"], "severity": "critical", "effect": "Heart failure, even from chewing leaves"},
    "tulips": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Vomiting, depression, especially from bulbs"},
    "azalea": {"toxic_to": ["dog", "cat"], "severity": "high", "effect": "Vomiting, weakness, cardiac failure in severe cases"},
    "english_ivy": {"toxic_to": ["dog", "cat"], "severity": "moderate", "effect": "Drooling, vomiting, abdominal pain"},
}

SAFE_PLANTS = [
    {"name": "Spider Plant", "safe_for": ["dog", "cat", "bird"], "benefit": "Air purifying, easy to grow, non-toxic"},
    {"name": "Boston Fern", "safe_for": ["dog", "cat"], "benefit": "Humidity boost, safe if chewed"},
    {"name": "Areca Palm", "safe_for": ["dog", "cat"], "benefit": "Excellent air purifier, tropical look"},
    {"name": "Calathea", "safe_for": ["dog", "cat"], "benefit": "Beautiful patterns, completely non-toxic"},
    {"name": "Bamboo Palm", "safe_for": ["dog", "cat"], "benefit": "Removes formaldehyde, pet-safe"},
    {"name": "African Violet", "safe_for": ["dog", "cat"], "benefit": "Colorful blooms, non-toxic, compact"},
    {"name": "Peperomia", "safe_for": ["dog", "cat"], "benefit": "Variety of textures, non-toxic, low maintenance"},
    {"name": "Haworthia", "safe_for": ["dog", "cat"], "benefit": "Succulent, non-toxic, needs minimal water"},
]

HAZARDOUS_ITEMS = {
    "candle": {"species": ["all"], "severity": "medium", "description": "Open flames risk burns and tail/fur fires", "solution": "Replace with flameless LED candles or enclosed hurricane lanterns"},
    "small_decorations": {"species": ["dog", "cat", "bird"], "severity": "medium", "description": "Small items can be swallowed causing intestinal blockage", "solution": "Remove items smaller than a tennis ball from pet-accessible surfaces"},
    "glass_vase": {"species": ["cat", "dog"], "severity": "medium", "description": "Can be knocked over causing glass shards on floor", "solution": "Use weighted ceramic or unbreakable vases, or secure with museum putty"},
    "electrical_cords": {"species": ["rabbit", "cat", "dog"], "severity": "high", "description": "Chewing cords causes electrical burns or electrocution", "solution": "Use cord covers, cable management boxes, or bitter apple spray on exposed wires"},
    "blinds_cords": {"species": ["cat", "bird"], "severity": "high", "description": "Looping cords are a strangulation risk", "solution": "Switch to cordless blinds or motorized window treatments"},
    "essential_oil_diffuser": {"species": ["cat", "bird"], "severity": "high", "description": "Many essential oils (tea tree, eucalyptus, peppermint) are toxic to cats and birds", "solution": "Use pet-safe alternatives only, or diffuse in pet-free rooms with ventilation"},
    "chocolate": {"species": ["dog"], "severity": "critical", "description": "Theobromine is toxic — dark chocolate is most dangerous", "solution": "Store all chocolate in sealed, elevated cabinets"},
    "recliner": {"species": ["cat", "small_dog"], "severity": "high", "description": "Pets can be crushed in reclining mechanisms", "solution": "Check underneath before reclining, or switch to non-reclining seating"},
}

FURNITURE_HAZARDS_BY_PET = {
    "dog": {
        "large": ["recliner", "glass_coffee_table_low"],
        "destructive": ["leather_sofa", "wooden_legs"],
        "general": ["trash_can_open", "low_shelves_with_food"],
    },
    "cat": {
        "climber": ["tall_unstable_shelves", "fragile_mantlepiece_items"],
        "general": ["open_washer_dryer", "toilet_lid_up", "unsecured_screens"],
    },
    "bird": {
        "general": ["ceiling_fans", "open_water", "mirrors_and_glass_doors", "non_stick_cookware_fumes"],
    },
    "rabbit": {
        "general": ["electrical_cords", "carpet_edges", "houseplants_at_floor_level"],
    },
}


class SafetyAnalyzer:
    def analyze(
        self,
        pets: list[dict],
        room_type: str,
        detected_objects: Optional[list[dict]] = None,
    ) -> dict:
        hazards = []
        plant_report = {"toxic": [], "safe_alternatives": []}
        safety_score = 9.0

        species_set = {p.get("species", "dog") for p in pets}

        if detected_objects:
            for obj in detected_objects:
                label = (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()

                if label in ("plant", "potted plant", "potted_plant"):
                    critical_plants = [
                        (name, info) for name, info in TOXIC_PLANTS.items()
                        if info["severity"] == "critical"
                        and any(s in info["toxic_to"] for s in species_set)
                    ]
                    for plant_name, info in critical_plants:
                        plant_report["toxic"].append({
                            "plant": plant_name.replace("_", " ").title(),
                            "toxic_to": [s for s in species_set if s in info["toxic_to"]],
                            "severity": info["severity"],
                            "effect": info["effect"],
                        })
                    if not plant_report.get("_advisory_added"):
                        plant_report["_advisory_added"] = True
                        plant_report["toxic"].append({
                            "plant": "Unidentified Plant",
                            "toxic_to": list(species_set),
                            "severity": "advisory",
                            "effect": "Many common houseplants are toxic to pets — identify your specific plant species to check safety",
                        })
                    plant_report["safe_alternatives"] = [
                        p for p in SAFE_PLANTS
                        if any(s in p["safe_for"] for s in species_set)
                    ][:5]

                for hazard_key, hazard_info in HAZARDOUS_ITEMS.items():
                    if hazard_key.replace("_", " ") in label or label in hazard_key:
                        if "all" in hazard_info["species"] or any(s in hazard_info["species"] for s in species_set):
                            hazards.append({
                                "hazard_type": "detected_item",
                                "severity": hazard_info["severity"],
                                "item": label,
                                "description": hazard_info["description"],
                                "solution": hazard_info["solution"],
                                "estimated_cost": self._estimate_fix_cost(hazard_info["severity"]),
                            })
                            safety_score -= {"critical": 2.5, "high": 1.5, "medium": 0.8, "low": 0.3}.get(hazard_info["severity"], 0.5)

        for pet in pets:
            species = pet.get("species", "dog")
            is_destructive = pet.get("is_destructive", False)
            climbs = pet.get("climbs_furniture", False)

            species_hazards = FURNITURE_HAZARDS_BY_PET.get(species, {})
            if is_destructive and "destructive" in species_hazards:
                for item in species_hazards["destructive"]:
                    hazards.append({
                        "hazard_type": "behavioral_risk",
                        "severity": "medium",
                        "item": item.replace("_", " "),
                        "description": f"Destructive {species} may damage {item.replace('_', ' ')}",
                        "solution": f"Use scratch-resistant or pet-proof alternatives",
                        "estimated_cost": 150,
                    })
                    safety_score -= 0.5

            if climbs and "climber" in species_hazards:
                for item in species_hazards["climber"]:
                    hazards.append({
                        "hazard_type": "climbing_risk",
                        "severity": "medium",
                        "item": item.replace("_", " "),
                        "description": f"Climbing {species} may topple {item.replace('_', ' ')}",
                        "solution": "Secure to wall with anti-tip straps or remove fragile items from high surfaces",
                        "estimated_cost": 25,
                    })
                    safety_score -= 0.5

        room_hazards = self._check_room_specific_hazards(room_type, species_set)
        hazards.extend(room_hazards)
        safety_score -= len(room_hazards) * 0.5

        plant_report.pop("_advisory_added", None)

        if hazards and is_available():
            species_str = ", ".join(species_set)
            for h in hazards[:5]:
                llm_solution = self._get_llm_solution(
                    h["item"], h["description"], room_type, species_str
                )
                if llm_solution:
                    h["solution"] = llm_solution

        return {
            "hazards": hazards,
            "plant_safety": plant_report,
            "safety_score": round(max(1.0, min(10.0, safety_score)), 1),
        }

    def _check_room_specific_hazards(self, room_type: str, species: set) -> list[dict]:
        hazards = []
        if room_type == "kitchen":
            if "dog" in species or "cat" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "high",
                    "item": "kitchen counters and stove",
                    "description": "Hot surfaces, sharp knives, and toxic foods (onions, garlic, grapes) accessible",
                    "solution": "Use stove guards, knife blocks in upper cabinets, and baby-lock on lower cabinets",
                    "estimated_cost": 45,
                })
            if "bird" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "critical",
                    "item": "non-stick cookware",
                    "description": "PTFE fumes from overheated non-stick pans are lethal to birds",
                    "solution": "Replace all non-stick cookware with stainless steel or cast iron",
                    "estimated_cost": 200,
                })
        elif room_type == "bathroom":
            hazards.append({
                "hazard_type": "room_specific",
                "severity": "medium",
                "item": "open toilet and cleaning products",
                "description": "Toilet water with chemicals, and accessible cleaning supplies are poisoning risks",
                "solution": "Keep toilet lid closed, store chemicals in locked cabinets",
                "estimated_cost": 15,
            })
        elif room_type == "bedroom":
            if "cat" in species or "dog" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "medium",
                    "item": "medications on nightstand",
                    "description": "Common medications (ibuprofen, acetaminophen, antidepressants) are highly toxic to pets",
                    "solution": "Store all medications in closed drawers or medicine cabinets",
                    "estimated_cost": 0,
                })
            if "cat" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "medium",
                    "item": "window without secure screen",
                    "description": "Cats can fall from open windows (high-rise syndrome)",
                    "solution": "Install secure window screens or limit opening width to under 5 cm",
                    "estimated_cost": 30,
                })
        elif room_type == "living_room":
            if "dog" in species or "cat" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "medium",
                    "item": "accessible trash and small objects",
                    "description": "Remote controls, batteries, coins, and rubber bands can cause choking or poisoning",
                    "solution": "Use pet-proof trash cans and keep small objects in closed containers",
                    "estimated_cost": 25,
                })
            if "bird" in species:
                hazards.append({
                    "hazard_type": "room_specific",
                    "severity": "high",
                    "item": "ceiling fans",
                    "description": "Ceiling fans are a collision hazard for free-flying birds",
                    "solution": "Turn off ceiling fans when birds are out of cage, or use fan guards",
                    "estimated_cost": 20,
                })
        return hazards

    def _get_llm_solution(self, item: str, description: str, room_type: str, species: str) -> str | None:
        prompt = (
            f"Pet safety: '{item}' in a {room_type} with {species}. "
            f"Issue: {description}. Give one specific, actionable solution in 1-2 sentences."
        )
        raw = get_llm_response_sync([{"role": "user", "content": prompt}], max_tokens=100)
        if raw and len(raw.strip()) > 10:
            return raw.strip()
        return None

    def _estimate_fix_cost(self, severity: str) -> float:
        return {"critical": 100, "high": 60, "medium": 30, "low": 10}.get(severity, 25)


safety_analyzer = SafetyAnalyzer()
