from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.house_project import HouseProject
from backend.app.models.room import Room
from backend.app.services.ai_service import ai_service
from backend.app.services.cost_service import cost_service


STYLE_COLOR_PALETTES = {
    "scandinavian": {
        "primary": ["#FFFFFF", "#F5F5DC", "#E8DCC8"],
        "accent": ["#A8C5DA", "#7BA38E", "#D4A574"],
        "materials": ["light oak", "birch", "pine", "linen", "wool", "ceramic"],
        "lighting": "warm ambient, natural light emphasis",
        "principles": [
            "Emphasize natural light and open spaces",
            "Use functional, minimal furniture with clean lines",
            "Layer neutral textures for warmth without clutter",
            "Incorporate natural materials throughout",
        ],
    },
    "modern": {
        "primary": ["#FFFFFF", "#F0F0F0", "#2C2C2C"],
        "accent": ["#C5A572", "#4A90D9", "#E85D4A"],
        "materials": ["glass", "steel", "concrete", "leather", "marble"],
        "lighting": "layered lighting with dimmers, track lights",
        "principles": [
            "Clean lines and geometric forms",
            "Open floor plans with minimal partitions",
            "Neutral base with bold accent pieces",
            "Technology-integrated design",
        ],
    },
    "minimalist": {
        "primary": ["#FFFFFF", "#FAFAFA", "#E0E0E0"],
        "accent": ["#000000", "#808080", "#C0B283"],
        "materials": ["concrete", "white oak", "glass", "cotton", "stone"],
        "lighting": "recessed lighting, hidden light sources",
        "principles": [
            "Less is more — every item must earn its place",
            "Monochromatic palette with one accent tone",
            "Built-in storage to eliminate visual clutter",
            "Focus on quality over quantity",
        ],
    },
    "industrial": {
        "primary": ["#3C3C3C", "#6B6B6B", "#A0A0A0"],
        "accent": ["#B87333", "#8B4513", "#DAA520"],
        "materials": ["exposed brick", "steel", "reclaimed wood", "iron", "concrete"],
        "lighting": "Edison bulbs, pendant metal fixtures",
        "principles": [
            "Celebrate raw, unfinished materials",
            "Expose structural elements (pipes, ducts, beams)",
            "Mix vintage and modern industrial pieces",
            "Use warm metals to soften hard edges",
        ],
    },
    "bohemian": {
        "primary": ["#F5E6D3", "#E8D5B7", "#D4C4A8"],
        "accent": ["#B8860B", "#CD5C5C", "#2E8B57", "#4682B4"],
        "materials": ["rattan", "macrame", "jute", "kilim", "cotton", "bamboo"],
        "lighting": "string lights, lanterns, candles",
        "principles": [
            "Layer patterns and textures freely",
            "Mix global influences and handmade pieces",
            "Incorporate abundant plants and greenery",
            "Embrace collected, eclectic curation",
        ],
    },
}

DEFAULT_PALETTE = {
    "primary": ["#FFFFFF", "#F0F0F0", "#D0D0D0"],
    "accent": ["#4A90D9", "#C5A572", "#6B8E6B"],
    "materials": ["wood", "fabric", "metal", "glass"],
    "lighting": "balanced ambient and task lighting",
    "principles": [
        "Create visual cohesion through repeated elements",
        "Balance proportions across rooms",
        "Use consistent flooring transitions",
        "Maintain a unified color temperature",
    ],
}

ROOM_TYPE_BUDGET_WEIGHTS = {
    "living_room": 0.30,
    "bedroom": 0.20,
    "kitchen": 0.25,
    "bathroom": 0.10,
    "dining_room": 0.15,
    "office": 0.15,
    "studio": 0.20,
    "hallway": 0.05,
}


class HouseDesignService:
    def build_shared_theme(
        self,
        style: str,
        color_preferences: Optional[list[str]] = None,
        material_preferences: Optional[list[str]] = None,
        lighting_preference: Optional[str] = None,
    ) -> dict:
        base = STYLE_COLOR_PALETTES.get(style, DEFAULT_PALETTE).copy()

        if color_preferences:
            base["primary"] = color_preferences[:3] or base["primary"]
            if len(color_preferences) > 3:
                base["accent"] = color_preferences[3:]

        if material_preferences:
            base["materials"] = material_preferences

        if lighting_preference:
            base["lighting"] = lighting_preference

        return {
            "style": style,
            "primary_colors": base["primary"],
            "accent_colors": base["accent"],
            "materials": base["materials"],
            "lighting": base["lighting"],
            "design_principles": base["principles"],
        }

    def allocate_room_budgets(
        self, total_budget: float, rooms: list[dict]
    ) -> dict:
        weights = {}
        total_weight = 0
        for room in rooms:
            room_type = room.get("room_type", "living_room")
            w = ROOM_TYPE_BUDGET_WEIGHTS.get(room_type, 0.15)
            weights[room.get("room_label", room_type)] = w
            total_weight += w

        allocations = {}
        for label, w in weights.items():
            normalized = w / total_weight if total_weight > 0 else 1 / len(rooms)
            allocations[label] = round(total_budget * normalized, 2)

        return allocations

    def build_room_prompt_with_theme(
        self, room_type: str, room_label: str, shared_theme: dict, room_budget: Optional[float] = None
    ) -> str:
        style = shared_theme.get("style", "modern")
        colors = ", ".join(shared_theme.get("primary_colors", []))
        accents = ", ".join(shared_theme.get("accent_colors", []))
        materials = ", ".join(shared_theme.get("materials", []))
        lighting = shared_theme.get("lighting", "ambient lighting")
        principles = " ".join(shared_theme.get("design_principles", []))

        prompt = (
            f"Design a {room_type.replace('_', ' ')} ({room_label}) in {style} style. "
            f"Primary colors: {colors}. Accent colors: {accents}. "
            f"Materials: {materials}. Lighting: {lighting}. "
            f"Design principles: {principles} "
            f"This room is part of a multi-room home design — ensure visual "
            f"continuity with other rooms using the same color palette, "
            f"material language, and design DNA."
        )

        if room_budget:
            prompt += f" Budget for this room: ${room_budget:.0f}."

        return prompt

    async def generate_all_room_designs(
        self,
        project: HouseProject,
        db: AsyncSession,
    ) -> list[dict]:
        shared_theme = project.shared_theme or {}
        budget_allocations = {}
        if project.budget:
            rooms_data = [
                {"room_type": rd.room_type, "room_label": rd.room_label}
                for rd in project.room_designs
            ]
            budget_allocations = self.allocate_room_budgets(project.budget, rooms_data)

        results = []
        total_cost = 0.0

        for room_design in project.room_designs:
            if room_design.status == "completed":
                if room_design.estimated_cost:
                    total_cost += room_design.estimated_cost
                continue

            room_design.status = "generating"
            await db.flush()

            room_budget = budget_allocations.get(room_design.room_label)
            prompt = self.build_room_prompt_with_theme(
                room_type=room_design.room_type,
                room_label=room_design.room_label,
                shared_theme=shared_theme,
                room_budget=room_budget,
            )

            room_analysis = {}
            if room_design.room_id:
                room_result = await db.execute(
                    select(Room).where(Room.id == room_design.room_id)
                )
                room = room_result.scalar_one_or_none()
                if room:
                    room_analysis = {
                        "room_type": room.room_type,
                        "area": room.area,
                        "detected_objects": room.detected_objects,
                        "segmentation_data": room.segmentation_data,
                        "image_url": room.image_url,
                    }

            try:
                ai_result = await ai_service.generate_design(
                    room_analysis=room_analysis or {"room_type": room_design.room_type},
                    style=shared_theme.get("style", "modern"),
                    prompt=prompt,
                    budget=room_budget,
                    preserve_layout=bool(room_design.room_id),
                )

                room_color_palette = {
                    "primary": shared_theme.get("primary_colors", []),
                    "accent": shared_theme.get("accent_colors", []),
                    "room_specific_accents": ai_result.get("color_palette"),
                }

                furniture_items = ai_result.get("furniture_list", [])
                room_cost_breakdown = cost_service.calculate_cost(
                    furniture_items=furniture_items if isinstance(furniture_items, list) else [],
                    room_area=room_analysis.get("area"),
                )

                room_design.generated_image_url = ai_result.get("image_url")
                room_design.room_color_palette = room_color_palette
                room_design.furniture_list = ai_result.get("furniture_list")
                room_design.estimated_cost = room_cost_breakdown["total_cost"]
                room_design.design_notes = ai_result.get("design_brief", "")
                room_design.ar_scene_data = ai_result.get("ar_scene_data")
                room_design.status = "completed"

                total_cost += room_cost_breakdown["total_cost"]

                results.append({
                    "room_label": room_design.room_label,
                    "status": "completed",
                    "estimated_cost": room_cost_breakdown["total_cost"],
                })

            except Exception as e:
                room_design.status = "failed"
                room_design.design_notes = f"Generation failed: {str(e)}"
                results.append({
                    "room_label": room_design.room_label,
                    "status": "failed",
                    "error": str(e),
                })

        project.total_estimated_cost = round(total_cost, 2)
        project.cost_breakdown_by_room = {
            rd.room_label: rd.estimated_cost
            for rd in project.room_designs
            if rd.estimated_cost
        }
        project.status = "completed"
        await db.flush()

        return results

    def generate_house_cost_report(
        self, project: HouseProject
    ) -> dict:
        room_costs = []
        for rd in project.room_designs:
            room_costs.append({
                "room_label": rd.room_label,
                "room_type": rd.room_type,
                "estimated_cost": rd.estimated_cost or 0,
                "status": rd.status,
            })

        total = sum(rc["estimated_cost"] for rc in room_costs)

        shared_elements = {
            "flooring_transitions": round(project.room_count * 150, 2),
            "consistent_paint": round(project.room_count * 200, 2),
            "lighting_fixtures": round(project.room_count * 120, 2),
            "total": round(project.room_count * 470, 2),
        }

        grand_total = total + shared_elements["total"]
        budget_status = "no_budget_set"
        savings = []

        if project.budget:
            if grand_total <= project.budget * 0.8:
                budget_status = "well_under_budget"
            elif grand_total <= project.budget:
                budget_status = "within_budget"
            elif grand_total <= project.budget * 1.1:
                budget_status = "slightly_over_budget"
            else:
                budget_status = "over_budget"
                savings.append("Consider phasing rooms — redesign high-impact areas first")
                savings.append("Use the same flooring throughout to reduce transition costs")
                savings.append("Buy furniture in bulk sets for multi-room discounts")
                savings.append("Prioritize DIY-friendly rooms to reduce labor costs")

        return {
            "project_id": str(project.id),
            "project_name": project.name,
            "style": project.style,
            "total_cost": round(grand_total, 2),
            "budget": project.budget,
            "budget_status": budget_status,
            "room_costs": room_costs,
            "shared_elements_cost": shared_elements,
            "savings_suggestions": savings if savings else None,
            "currency": project.currency,
        }


house_design_service = HouseDesignService()
