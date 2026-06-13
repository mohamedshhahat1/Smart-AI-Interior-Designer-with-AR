from typing import Optional


STYLE_PROMPTS = {
    "modern": "modern interior design, clean lines, neutral colors, open space, contemporary furniture",
    "scandinavian": "scandinavian interior design, light wood, white walls, cozy textiles, minimalist, hygge atmosphere",
    "minimalist": "minimalist interior design, bare essentials, monochromatic palette, clean surfaces, zen-like simplicity",
    "industrial": "industrial interior design, exposed brick, metal fixtures, raw materials, open ductwork, loft style",
    "bohemian": "bohemian interior design, eclectic patterns, warm colors, layered textiles, plants, artistic decor",
    "mid_century_modern": "mid-century modern interior, retro furniture, organic shapes, warm wood tones, iconic design pieces",
    "contemporary": "contemporary interior design, current trends, sleek materials, bold accents, sophisticated elegance",
    "traditional": "traditional interior design, classic furniture, rich fabrics, warm wood, ornate details, timeless elegance",
    "rustic": "rustic interior design, natural wood, stone accents, warm earth tones, cozy cabin feel",
    "art_deco": "art deco interior design, geometric patterns, luxurious materials, bold colors, glamorous fixtures",
    "japanese": "japanese interior design, wabi-sabi aesthetic, natural materials, tatami, sliding doors, zen garden influence",
    "coastal": "coastal interior design, ocean-inspired colors, light fabrics, natural textures, beach house atmosphere",
    "farmhouse": "farmhouse interior design, shiplap walls, vintage accents, comfortable furnishings, country charm",
    "mediterranean": "mediterranean interior design, terracotta tiles, wrought iron, warm stucco walls, arched doorways",
}

QUALITY_SUFFIX = (
    "photorealistic interior photo, realistic scale, detailed materials, natural lighting"
)

NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, deformed furniture, unrealistic proportions, "
    "watermark, text, oversaturated, cartoon, anime, sketch, painting style, "
    "people, animals, outdoors"
)

ROOM_FURNISHING_PROMPTS = {
    "living_room": "furnished with a sofa, coffee table, area rug, side tables, and warm lighting",
    "bedroom": "furnished with a bed, nightstands, wardrobe, area rug, and warm lighting",
    "dining_room": "furnished with a dining table, dining chairs, pendant light, and sideboard",
    "kitchen": "furnished kitchen with cabinets, worktops, appliances, and practical lighting",
    "office": "furnished with a desk, ergonomic chair, storage, shelving, and task lighting",
    "bathroom": "finished bathroom with vanity, mirror, storage, fixtures, and layered lighting",
}


class PromptBuilder:
    def build_design_prompt(
        self,
        style: str,
        room_type: str,
        user_prompt: Optional[str] = None,
        detected_objects: Optional[list[str]] = None,
        budget: Optional[float] = None,
    ) -> dict:
        style_key = style.strip().lower().replace("-", "_").replace(" ", "_")
        style_base = STYLE_PROMPTS.get(style_key, STYLE_PROMPTS["modern"])

        room_key = room_type.strip().lower().replace("-", "_").replace(" ", "_")
        room_context = f"{room_key.replace('_', ' ')} interior"

        furnishing = ROOM_FURNISHING_PROMPTS.get(
            room_key,
            "fully furnished with appropriately scaled furniture, decor, and lighting",
        )
        parts = [style_base, room_context, furnishing]

        if user_prompt:
            parts.append(user_prompt)

        if detected_objects:
            furniture_context = ", ".join(detected_objects[:6])
            parts.append(f"featuring {furniture_context}")

        if budget:
            if budget < 2000:
                parts.append("budget-friendly decor, affordable furniture")
            elif budget < 5000:
                parts.append("mid-range quality furnishings")
            else:
                parts.append("premium quality, luxury furnishings")

        parts.append(QUALITY_SUFFIX)

        positive_prompt = ", ".join(parts)

        return {
            "positive": positive_prompt,
            "negative": NEGATIVE_PROMPT,
            "style": style,
            "room_type": room_type,
            "is_empty_room": not detected_objects,
        }

    def build_enhancement_prompt(
        self, current_style: str, instruction: str
    ) -> dict:
        style_key = current_style.strip().lower().replace("-", "_").replace(" ", "_")
        style_base = STYLE_PROMPTS.get(style_key, "")

        positive = f"{style_base}, {instruction}, {QUALITY_SUFFIX}"

        return {
            "positive": positive,
            "negative": NEGATIVE_PROMPT,
            "instruction": instruction,
        }


prompt_builder = PromptBuilder()
