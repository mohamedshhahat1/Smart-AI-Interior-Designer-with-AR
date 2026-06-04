from typing import Optional


PET_ZONES = {
    "dog": {
        "sleeping": {
            "zone_type": "rest",
            "description": "A dedicated sleeping area away from drafts and high-traffic paths",
            "items": ["orthopedic dog bed", "washable blanket", "water bowl"],
            "location_preference": "quiet corner, away from entrance",
            "cost": 85,
        },
        "feeding": {
            "zone_type": "dining",
            "description": "Designated feeding station with easy-clean flooring underneath",
            "items": ["elevated food bowls", "silicone feeding mat", "water fountain"],
            "location_preference": "kitchen or utility area, away from foot traffic",
            "cost": 55,
        },
        "play": {
            "zone_type": "activity",
            "description": "Open area for play with durable toys and interactive puzzles",
            "items": ["toy basket", "chew-resistant toys", "puzzle feeder"],
            "location_preference": "living room open area, clear of fragile items",
            "cost": 40,
        },
        "lookout": {
            "zone_type": "enrichment",
            "description": "Window perch or elevated spot for watching outside activity",
            "items": ["window-level platform or cushion", "non-slip mat"],
            "location_preference": "near a window with outdoor view",
            "cost": 35,
        },
    },
    "cat": {
        "sleeping": {
            "zone_type": "rest",
            "description": "Elevated cozy nook — cats prefer sleeping above ground level",
            "items": ["cat tree with bed", "heated cat bed", "soft blanket"],
            "location_preference": "elevated shelf, top of cat tree, or warm sunny spot",
            "cost": 70,
        },
        "climbing": {
            "zone_type": "activity",
            "description": "Vertical space with cat shelves, trees, and perches for climbing and exercise",
            "items": ["cat tree", "wall-mounted cat shelves", "sisal scratching post"],
            "location_preference": "along walls, near windows, corner cat tree",
            "cost": 120,
        },
        "scratching": {
            "zone_type": "enrichment",
            "description": "Designated scratching stations to protect furniture",
            "items": ["vertical scratching post", "horizontal scratch pad", "cardboard scratcher"],
            "location_preference": "near furniture they tend to scratch, by sleeping area",
            "cost": 35,
        },
        "hiding": {
            "zone_type": "rest",
            "description": "Enclosed hiding spots for when they need alone time and security",
            "items": ["cat cave", "covered cat bed", "cardboard box hideaway"],
            "location_preference": "quiet area, under table, or in a closet nook",
            "cost": 30,
        },
        "window_perch": {
            "zone_type": "enrichment",
            "description": "Window-mounted seat for bird watching and sunbathing",
            "items": ["suction cup window perch", "window-sill cushion"],
            "location_preference": "sunniest window with outdoor view",
            "cost": 25,
        },
        "litter": {
            "zone_type": "hygiene",
            "description": "Discreet litter box area with good ventilation and privacy",
            "items": ["enclosed litter box", "litter mat", "odor absorber"],
            "location_preference": "bathroom corner, utility room, or dedicated cabinet",
            "cost": 50,
        },
    },
    "bird": {
        "cage_area": {
            "zone_type": "habitat",
            "description": "Primary cage placement with natural light but away from drafts and kitchen fumes",
            "items": ["appropriately sized cage", "perch variety", "food/water dishes", "cage cover"],
            "location_preference": "living room wall, away from kitchen and windows that open",
            "cost": 150,
        },
        "free_flight": {
            "zone_type": "activity",
            "description": "Safe room for supervised out-of-cage time with ceiling fans off",
            "items": ["play gym", "foraging toys", "bird-safe perch stand"],
            "location_preference": "room with closed windows and no ceiling fans",
            "cost": 60,
        },
    },
    "rabbit": {
        "enclosure": {
            "zone_type": "habitat",
            "description": "Spacious pen area with hiding spots and soft flooring",
            "items": ["exercise pen", "hay rack", "water bottle", "hiding house"],
            "location_preference": "quiet room corner, away from loud speakers and TV",
            "cost": 80,
        },
        "exercise": {
            "zone_type": "activity",
            "description": "Bunny-proofed open area for exercise and exploration",
            "items": ["cord protectors", "tunnel toys", "digging box"],
            "location_preference": "living room floor, cords and cables fully protected",
            "cost": 45,
        },
    },
}

MATERIAL_RECOMMENDATIONS = {
    "flooring": {
        "dog": {"recommended": "Luxury vinyl plank, ceramic tile, or sealed concrete", "avoid": "Hardwood (scratches from nails), carpet (stains and odor)", "reason": "Scratch-resistant, waterproof, easy to clean accidents"},
        "cat": {"recommended": "Luxury vinyl plank, laminate, or tile", "avoid": "Loop-pile carpet (snags claws), unsealed wood", "reason": "Resists scratches and is easy to clean litter tracking"},
        "bird": {"recommended": "Tile, vinyl, or sealed wood", "avoid": "Carpet (traps feathers and dander)", "reason": "Easy to sweep droppings and feathers"},
        "rabbit": {"recommended": "Vinyl with area rugs for traction", "avoid": "Slippery surfaces without rugs (splayed legs)", "reason": "Rabbits need traction — bare tile causes injuries"},
    },
    "upholstery": {
        "dog": {"recommended": "Crypton fabric, microfiber, or outdoor fabric (Sunbrella)", "avoid": "Silk, velvet, loosely woven textiles", "reason": "Stain-resistant, durable against claws and drool"},
        "cat": {"recommended": "Microfiber, tight-weave canvas, ultrasuede", "avoid": "Leather (visible scratches), linen, chenille", "reason": "Resists snagging from claws, easy to lint-roll"},
    },
    "rugs": {
        "dog": {"recommended": "Indoor/outdoor rugs, flat-weave washable rugs", "avoid": "Shag, high-pile, silk rugs", "reason": "Machine washable, resists stains and digging"},
        "cat": {"recommended": "Low-pile, sisal, or flat-weave rugs", "avoid": "Loop-pile (catches claws), delicate fibers", "reason": "Won't trap litter, resists snagging"},
    },
    "curtains": {
        "cat": {"recommended": "Short curtains, roman shades, or top-down blinds", "avoid": "Floor-length drapes (climbing invitation)", "reason": "Prevents climbing and reduces fabric snagging"},
        "bird": {"recommended": "Short blinds or shutters", "avoid": "Sheer curtains with loose threads (entanglement risk)", "reason": "Birds can get tangled in loose fabric threads"},
    },
}

CLEANING_TIPS = {
    "dog": [
        "Vacuum 2-3 times per week with a HEPA pet-hair vacuum",
        "Wash pet bedding weekly in hot water",
        "Keep enzymatic cleaner spray for accident spots — it breaks down odor-causing proteins",
        "Place washable mats at entry points to catch muddy paws",
        "Use a robot vacuum daily if your dog sheds heavily",
        "Wipe paws with pet-safe wipes after outdoor walks",
    ],
    "cat": [
        "Scoop litter box daily, full clean weekly",
        "Place a litter-catching mat under and around the litter box",
        "Vacuum upholstery 2x per week with a pet-hair attachment",
        "Use a lint roller on soft furnishings between vacuums",
        "Wash window perch covers and cat bed covers biweekly",
        "Use air purifier with HEPA filter to reduce dander and litter dust",
    ],
    "bird": [
        "Clean cage bottom daily — replace liner paper",
        "Wash food and water dishes daily to prevent bacterial growth",
        "Vacuum around cage daily for seed hulls and feather dust",
        "Deep clean cage with bird-safe disinfectant weekly",
        "Use an air purifier — bird dander is a significant allergen",
    ],
    "rabbit": [
        "Spot-clean litter area daily",
        "Sweep hay and droppings from exercise area daily",
        "Wash fleece liners and blankets weekly",
        "Vinegar-water solution is safe for cleaning rabbit areas",
    ],
}


class ZonePlanner:
    def plan_zones(
        self,
        pets: list[dict],
        room_type: str,
        room_dimensions: Optional[dict] = None,
    ) -> dict:
        zones = []
        materials = []
        tips = []
        total_cost = 0

        species_seen = set()
        for pet in pets:
            species = pet.get("species", "dog")
            if species in species_seen:
                continue
            species_seen.add(species)

            species_zones = PET_ZONES.get(species, {})
            for zone_key, zone_data in species_zones.items():
                zones.append({
                    "zone_name": f"{pet.get('name', species).title()}'s {zone_key.replace('_', ' ').title()}",
                    "zone_type": zone_data["zone_type"],
                    "location": zone_data["location_preference"],
                    "description": zone_data["description"],
                    "items_needed": zone_data["items"],
                    "estimated_cost": zone_data["cost"],
                })
                total_cost += zone_data["cost"]

            species_materials = MATERIAL_RECOMMENDATIONS.copy()
            for category in ["flooring", "upholstery", "rugs", "curtains"]:
                if species in species_materials.get(category, {}):
                    materials.append({
                        "category": category,
                        **species_materials[category][species],
                    })

            tips.extend(CLEANING_TIPS.get(species, []))

        unique_tips = list(dict.fromkeys(tips))

        comfort = 7.0
        durability = 7.0
        cleanliness = 7.0

        for pet in pets:
            if pet.get("sheds_fur"):
                cleanliness -= 0.5
            if pet.get("is_destructive"):
                durability -= 1.0
            if pet.get("energy_level") == "high":
                comfort += 0.3
            if pet.get("climbs_furniture"):
                durability -= 0.5

        return {
            "zones": zones,
            "materials": materials,
            "cleaning_tips": unique_tips,
            "comfort_score": round(max(1.0, min(10.0, comfort)), 1),
            "durability_score": round(max(1.0, min(10.0, durability)), 1),
            "cleanliness_score": round(max(1.0, min(10.0, cleanliness)), 1),
            "total_cost": total_cost,
        }


zone_planner = ZonePlanner()
