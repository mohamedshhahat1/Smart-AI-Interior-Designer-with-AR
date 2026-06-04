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
    "professional interior photography, 8k resolution, perfect lighting, "
    "architectural digest quality, photorealistic, detailed textures"
)

NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, deformed furniture, unrealistic proportions, "
    "watermark, text, oversaturated, cartoon, anime, sketch, painting style, "
    "people, animals, outdoors"
)


class PromptBuilder:
    def build_design_prompt(
        self,
        style: str,
        room_type: str,
        user_prompt: Optional[str] = None,
        detected_objects: Optional[list[str]] = None,
        budget: Optional[float] = None,
    ) -> dict:
        style_base = STYLE_PROMPTS.get(style, STYLE_PROMPTS["modern"])

        room_context = f"{room_type.replace('_', ' ')} interior"

        parts = [style_base, room_context]

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
        }

    def build_enhancement_prompt(
        self, current_style: str, instruction: str
    ) -> dict:
        style_base = STYLE_PROMPTS.get(current_style, "")

        positive = f"{style_base}, {instruction}, {QUALITY_SUFFIX}"

        return {
            "positive": positive,
            "negative": NEGATIVE_PROMPT,
            "instruction": instruction,
        }


prompt_builder = PromptBuilder()
