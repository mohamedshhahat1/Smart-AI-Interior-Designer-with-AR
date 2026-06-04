from typing import Optional


class ThemeUnifier:
    """Ensures visual consistency across multiple rooms in a house design."""

    def create_unified_prompt_set(
        self,
        rooms: list[dict],
        shared_theme: dict,
        budget_per_room: Optional[dict] = None,
    ) -> list[dict]:
        style = shared_theme.get("style", "modern")
        theme_dna = self._build_theme_dna(shared_theme)

        prompts = []
        for room in rooms:
            room_type = room.get("room_type", "room")
            room_label = room.get("room_label", room_type)
            room_budget = (budget_per_room or {}).get(room_label)

            base_prompt = self._build_room_base_prompt(room_type, style)
            room_specific = self._get_room_specific_elements(room_type, style)

            full_prompt = (
                f"{base_prompt} {theme_dna} {room_specific} "
                f"Ensure this {room_label} connects visually with adjacent rooms "
                f"through shared color temperature, material language, and "
                f"consistent trim/molding details."
            )

            if room_budget:
                full_prompt += f" Budget: ${room_budget:.0f}."

            prompts.append({
                "room_label": room_label,
                "room_type": room_type,
                "positive": full_prompt + ", " + QUALITY_SUFFIX,
                "negative": CONSISTENCY_NEGATIVE,
                "theme_dna": theme_dna,
            })

        return prompts

    def _build_theme_dna(self, shared_theme: dict) -> str:
        colors = shared_theme.get("primary_colors", [])
        accents = shared_theme.get("accent_colors", [])
        materials = shared_theme.get("materials", [])
        lighting = shared_theme.get("lighting", "ambient")
        principles = shared_theme.get("design_principles", [])

        return (
            f"HOUSE THEME DNA: "
            f"primary palette [{', '.join(colors)}], "
            f"accent palette [{', '.join(accents)}], "
            f"material language [{', '.join(materials)}], "
            f"lighting scheme [{lighting}], "
            f"design rules [{'; '.join(principles[:3])}]. "
            f"Every room MUST reference this DNA for visual unity."
        )

    def _build_room_base_prompt(self, room_type: str, style: str) -> str:
        room_name = room_type.replace("_", " ")
        return (
            f"Interior design photograph of a {room_name} in {style} style, "
            f"professional architectural photography"
        )

    def _get_room_specific_elements(self, room_type: str, style: str) -> str:
        elements = ROOM_SPECIFIC_ELEMENTS.get(room_type, {})
        style_elements = elements.get(style, elements.get("default", ""))
        return style_elements

    def validate_cross_room_consistency(
        self, room_designs: list[dict], shared_theme: dict
    ) -> dict:
        issues = []
        suggestions = []

        expected_colors = set(
            shared_theme.get("primary_colors", [])
            + shared_theme.get("accent_colors", [])
        )
        expected_materials = set(shared_theme.get("materials", []))

        for design in room_designs:
            room_label = design.get("room_label", "Unknown")
            palette = design.get("room_color_palette", {})

            room_colors = set(
                palette.get("primary", []) + palette.get("accent", [])
            )
            if room_colors and not room_colors.intersection(expected_colors):
                issues.append(
                    f"{room_label}: color palette deviates from house theme"
                )

        if not issues:
            suggestions.append("All rooms maintain consistent color palette")
        else:
            suggestions.append("Consider regenerating inconsistent rooms")

        styles_used = set(d.get("style") for d in room_designs if d.get("style"))
        if len(styles_used) > 1:
            issues.append(f"Mixed styles detected: {', '.join(styles_used)}")
            suggestions.append("Regenerate with a single unified style")
        else:
            suggestions.append("Style consistency verified across all rooms")

        return {
            "is_consistent": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "rooms_checked": len(room_designs),
        }

    def generate_transition_recommendations(
        self, room_sequence: list[dict]
    ) -> list[dict]:
        transitions = []
        for i in range(len(room_sequence) - 1):
            current = room_sequence[i]
            next_room = room_sequence[i + 1]

            transition = {
                "from_room": current.get("room_label", f"Room {i+1}"),
                "to_room": next_room.get("room_label", f"Room {i+2}"),
                "recommendations": self._get_transition_tips(
                    current.get("room_type", ""),
                    next_room.get("room_type", ""),
                ),
            }
            transitions.append(transition)

        return transitions

    def _get_transition_tips(self, from_type: str, to_type: str) -> list[str]:
        tips = [
            "Use the same flooring material or a complementary transition strip",
            "Maintain consistent baseboards and crown molding profiles",
            "Keep wall color temperature consistent (warm-to-warm or cool-to-cool)",
        ]

        if from_type == "living_room" and to_type == "dining_room":
            tips.append("Consider an open-plan connection with a visual divider like a rug")
        elif from_type in ("bedroom", "office") and to_type == "hallway":
            tips.append("Use the hallway as a neutral bridge with muted tones")
        elif "kitchen" in (from_type, to_type):
            tips.append("Transition from kitchen tile to adjacent room flooring with a flush threshold")

        return tips


QUALITY_SUFFIX = (
    "professional interior photography, 8k resolution, perfect lighting, "
    "architectural digest quality, photorealistic, detailed textures, "
    "consistent with multi-room house design"
)

CONSISTENCY_NEGATIVE = (
    "blurry, low quality, distorted, deformed furniture, unrealistic proportions, "
    "watermark, text, oversaturated, cartoon, anime, sketch, painting style, "
    "people, animals, outdoors, mismatched style, inconsistent colors, "
    "clashing materials, different design language"
)

ROOM_SPECIFIC_ELEMENTS = {
    "living_room": {
        "scandinavian": "comfortable seating area, light wood coffee table, cozy textiles, indoor plants, large windows with natural light",
        "modern": "sleek sofa, geometric coffee table, statement art piece, recessed lighting",
        "default": "comfortable sofa, coffee table, entertainment area, ambient lighting",
    },
    "bedroom": {
        "scandinavian": "platform bed with linen bedding, bedside tables with warm lamps, soft rug, minimal wall decor",
        "modern": "upholstered bed frame, floating nightstands, accent wall, indirect lighting",
        "default": "bed with quality bedding, nightstands, wardrobe, soft lighting",
    },
    "kitchen": {
        "scandinavian": "white cabinetry, butcher block counters, open shelving, pendant lights over island",
        "modern": "handleless cabinets, quartz countertops, integrated appliances, under-cabinet lighting",
        "default": "functional cabinetry, quality countertops, task lighting, organized storage",
    },
    "office": {
        "scandinavian": "simple desk with wood top, ergonomic chair, wall-mounted shelves, desk lamp",
        "modern": "standing desk option, leather chair, built-in bookcase, focused task lighting",
        "default": "desk workspace, comfortable chair, storage, proper task lighting",
    },
    "bathroom": {
        "scandinavian": "white tiles, wooden vanity, frameless mirror, warm towel accents",
        "modern": "floating vanity, large format tiles, walk-in shower, backlit mirror",
        "default": "clean vanity, good mirror, organized storage, proper ventilation",
    },
    "dining_room": {
        "scandinavian": "oak dining table, mixed chairs, pendant light over table, sideboard",
        "modern": "glass or marble dining table, upholstered chairs, chandelier, minimal buffet",
        "default": "dining table with seating, overhead lighting, serving storage",
    },
}


theme_unifier = ThemeUnifier()
