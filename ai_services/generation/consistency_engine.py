from typing import Optional

from ai_services.utils.image_processing import extract_dominant_colors
from ai_services.utils.llm_client import get_llm_response_sync, parse_llm_json, is_available


class ConsistencyEngine:
    """Post-generation validator ensuring cross-room visual coherence."""

    def __init__(self):
        self.color_tolerance = 0.15
        self.material_keywords = {}

    def analyze_design_consistency(
        self, room_designs: list[dict], shared_theme: dict
    ) -> dict:
        color_analysis = self._analyze_color_consistency(room_designs, shared_theme)
        style_analysis = self._analyze_style_consistency(room_designs, shared_theme)
        material_analysis = self._analyze_material_consistency(room_designs, shared_theme)

        overall_score = (
            color_analysis["score"] * 0.4
            + style_analysis["score"] * 0.35
            + material_analysis["score"] * 0.25
        )

        return {
            "overall_score": round(overall_score, 2),
            "rating": self._score_to_rating(overall_score),
            "color_consistency": color_analysis,
            "style_consistency": style_analysis,
            "material_consistency": material_analysis,
            "recommendations": self._generate_recommendations(
                color_analysis, style_analysis, material_analysis
            ),
        }

    def _analyze_color_consistency(
        self, room_designs: list[dict], shared_theme: dict
    ) -> dict:
        theme_colors = (
            shared_theme.get("primary_colors", [])
            + shared_theme.get("accent_colors", [])
        )

        if not theme_colors:
            return {"score": 0.5, "details": "No theme colors defined"}

        rooms_aligned = 0
        room_details = []

        for design in room_designs:
            palette = design.get("room_color_palette", {})
            room_colors = palette.get("primary", []) + palette.get("accent", [])

            if not room_colors:
                room_details.append({
                    "room": design.get("room_label"),
                    "aligned": False,
                    "note": "No color data available",
                })
                continue

            overlap = len(set(room_colors) & set(theme_colors))
            aligned = overlap > 0

            if aligned:
                rooms_aligned += 1

            room_details.append({
                "room": design.get("room_label"),
                "aligned": aligned,
                "shared_colors": overlap,
            })

        score = rooms_aligned / len(room_designs) if room_designs else 0

        return {
            "score": round(score, 2),
            "rooms_aligned": rooms_aligned,
            "total_rooms": len(room_designs),
            "details": room_details,
        }

    def _analyze_style_consistency(
        self, room_designs: list[dict], shared_theme: dict
    ) -> dict:
        target_style = shared_theme.get("style", "")

        matched = 0
        details = []

        for design in room_designs:
            furniture = design.get("furniture_list", [])
            if not furniture:
                details.append({
                    "room": design.get("room_label"),
                    "style_match": True,
                    "note": "No furniture data to validate",
                })
                matched += 1
                continue

            if isinstance(furniture, list):
                styles = [
                    item.get("style", "").lower()
                    for item in furniture
                    if isinstance(item, dict)
                ]
                style_match = any(target_style.lower() in s for s in styles) if styles else True
            else:
                style_match = True

            if style_match:
                matched += 1

            details.append({
                "room": design.get("room_label"),
                "style_match": style_match,
            })

        score = matched / len(room_designs) if room_designs else 0

        return {
            "score": round(score, 2),
            "target_style": target_style,
            "rooms_matched": matched,
            "total_rooms": len(room_designs),
            "details": details,
        }

    def _analyze_material_consistency(
        self, room_designs: list[dict], shared_theme: dict
    ) -> dict:
        target_materials = [m.lower() for m in shared_theme.get("materials", [])]

        if not target_materials:
            return {"score": 0.5, "details": "No target materials defined"}

        matched_rooms = 0
        details = []

        for design in room_designs:
            furniture = design.get("furniture_list", [])
            room_materials = set()

            if isinstance(furniture, list):
                for item in furniture:
                    if isinstance(item, dict):
                        mat = item.get("material", "").lower()
                        if mat:
                            room_materials.add(mat)

            overlap = len(room_materials & set(target_materials))
            matched = overlap > 0 or not room_materials

            if matched:
                matched_rooms += 1

            details.append({
                "room": design.get("room_label"),
                "materials_aligned": matched,
                "shared_materials": overlap,
            })

        score = matched_rooms / len(room_designs) if room_designs else 0

        return {
            "score": round(score, 2),
            "target_materials": target_materials,
            "rooms_aligned": matched_rooms,
            "details": details,
        }

    def _score_to_rating(self, score: float) -> str:
        if score >= 0.9:
            return "excellent"
        if score >= 0.75:
            return "good"
        if score >= 0.6:
            return "fair"
        if score >= 0.4:
            return "needs_improvement"
        return "inconsistent"

    def _generate_recommendations(
        self,
        color_analysis: dict,
        style_analysis: dict,
        material_analysis: dict,
    ) -> list[str]:
        recs = []

        if color_analysis.get("score", 0) < 0.7:
            recs.append(
                "Some rooms deviate from the shared color palette — regenerate "
                "with stricter color constraints to improve visual flow"
            )

        if style_analysis.get("score", 0) < 0.7:
            recs.append(
                f"Not all furniture matches the {style_analysis.get('target_style', '')} "
                f"style — review furniture selections for consistency"
            )

        if material_analysis.get("score", 0) < 0.7:
            recs.append(
                "Material choices vary across rooms — consider using shared "
                "materials (same wood tone, metal finish) for cohesion"
            )

        if not recs:
            recs.append(
                "Your house design shows excellent cross-room consistency. "
                "The unified theme is well-applied."
            )

        return recs

    def suggest_shared_elements(
        self, room_types: list[str], style: str
    ) -> dict:
        result = {
            "flooring": self._suggest_flooring(style),
            "wall_treatment": self._suggest_walls(style),
            "trim_and_molding": self._suggest_trim(style),
            "door_hardware": self._suggest_hardware(style),
            "lighting_temperature": self._suggest_light_temp(style),
        }

        generic_count = sum(
            1 for v in result.values()
            if (isinstance(v, dict) and "Consistent" in v.get("note", ""))
            or (isinstance(v, str) and v.startswith("Consistent"))
        )
        if generic_count >= 3 and is_available():
            llm_result = self._llm_suggest_shared_elements(room_types, style)
            if llm_result:
                result.update(llm_result)

        return result

    def _llm_suggest_shared_elements(
        self, room_types: list[str], style: str
    ) -> dict | None:
        rooms_str = ", ".join(room_types) if room_types else "general rooms"
        prompt = (
            f"For a '{style}' style home with {rooms_str}, suggest shared design elements.\n"
            f"Return a JSON object with these keys:\n"
            f'- "flooring": {{"material": "...", "color": "...", "note": "..."}}\n'
            f'- "wall_treatment": {{"treatment": "...", "accent": "...", "note": "..."}}\n'
            f'- "trim_and_molding": "one line description"\n'
            f'- "door_hardware": "one line description"\n'
            f'- "lighting_temperature": "one line description"\n'
            f"Be specific to the {style} style."
        )
        raw = get_llm_response_sync([{"role": "user", "content": prompt}], max_tokens=400)
        data = parse_llm_json(raw)
        if isinstance(data, dict) and any(k in data for k in ("flooring", "wall_treatment")):
            return data
        return None

    def _suggest_flooring(self, style: str) -> dict:
        options = {
            "scandinavian": {"material": "Light oak hardwood", "color": "Natural blonde", "note": "Wide planks throughout, tile only in bathroom"},
            "modern": {"material": "Large format porcelain", "color": "Light grey", "note": "Seamless transitions between rooms"},
            "industrial": {"material": "Polished concrete", "color": "Natural grey", "note": "Area rugs for warmth in living spaces"},
            "minimalist": {"material": "White oak engineered", "color": "Pale natural", "note": "Consistent grain direction across rooms"},
            "bohemian": {"material": "Terracotta tile or reclaimed wood", "color": "Warm earth tones", "note": "Layer with kilim and jute rugs"},
        }
        return options.get(style, {"material": "Hardwood", "color": "Medium tone", "note": "Consistent throughout"})

    def _suggest_walls(self, style: str) -> dict:
        options = {
            "scandinavian": {"treatment": "Matte white paint", "accent": "Light wood paneling", "note": "Keep walls predominantly white"},
            "modern": {"treatment": "Eggshell neutral paint", "accent": "Textured accent wall", "note": "One accent wall per room max"},
            "industrial": {"treatment": "Exposed brick or concrete render", "accent": "Raw plaster sections", "note": "Embrace imperfections"},
        }
        return options.get(style, {"treatment": "Neutral paint", "accent": "Feature wall", "note": "Consistent base color"})

    def _suggest_trim(self, style: str) -> str:
        options = {
            "scandinavian": "Minimal white trim, no ornate molding",
            "modern": "Clean-line shadow gap trim, no crown molding",
            "traditional": "Classic crown molding and chair rail throughout",
            "industrial": "No trim — exposed junctions and raw edges",
        }
        return options.get(style, "Consistent trim profile throughout")

    def _suggest_hardware(self, style: str) -> str:
        options = {
            "scandinavian": "Brushed stainless steel, minimal profile",
            "modern": "Matte black lever handles throughout",
            "industrial": "Aged brass or iron hardware",
            "bohemian": "Mixed vintage brass handles",
        }
        return options.get(style, "Consistent metal finish across all rooms")

    def _suggest_light_temp(self, style: str) -> str:
        options = {
            "scandinavian": "2700K-3000K warm white throughout",
            "modern": "3000K-3500K neutral white, dimmable",
            "industrial": "2200K-2700K warm Edison-style",
            "minimalist": "3000K neutral, hidden fixtures",
        }
        return options.get(style, "3000K consistent color temperature")


consistency_engine = ConsistencyEngine()
