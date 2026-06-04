from typing import Optional


REGIONAL_MULTIPLIERS = {
    "US": 1.0,
    "EU": 1.15,
    "UK": 1.25,
    "ME": 0.85,
    "ASIA": 0.70,
}

STYLE_COST_FACTOR = {
    "minimalist": 0.85,
    "scandinavian": 1.0,
    "modern": 1.1,
    "contemporary": 1.15,
    "industrial": 0.95,
    "bohemian": 0.90,
    "mid_century_modern": 1.3,
    "traditional": 1.2,
    "rustic": 1.0,
    "art_deco": 1.5,
    "japanese": 1.1,
    "coastal": 0.95,
    "farmhouse": 0.90,
    "mediterranean": 1.2,
}


class CostCalculator:
    def calculate_full_cost(
        self,
        furniture_items: list[dict],
        room_area: float,
        style: str = "modern",
        region: str = "US",
        include_labor: bool = True,
        include_flooring: bool = False,
        include_painting: bool = True,
    ) -> dict:
        regional_mult = REGIONAL_MULTIPLIERS.get(region, 1.0)
        style_mult = STYLE_COST_FACTOR.get(style, 1.0)

        furniture_cost = sum(item.get("price", 0) for item in furniture_items)
        furniture_cost *= style_mult

        painting_cost = 0.0
        if include_painting:
            wall_area = room_area * 2.8 * 0.7
            painting_cost = wall_area * 12.0

        flooring_cost = 0.0
        if include_flooring:
            flooring_cost = room_area * 45.0

        decoration_cost = room_area * 15.0 * style_mult

        lighting_cost = max(3, len(furniture_items)) * 75.0

        labor_cost = 0.0
        if include_labor:
            assembly_hours = len(furniture_items) * 1.5
            labor_cost = assembly_hours * 55.0
            if include_painting:
                labor_cost += (room_area * 0.4) * 40.0
            if include_flooring:
                labor_cost += (room_area * 0.5) * 50.0

        subtotal = (
            furniture_cost + painting_cost + flooring_cost
            + decoration_cost + lighting_cost + labor_cost
        )
        total = subtotal * regional_mult

        return {
            "furniture": round(furniture_cost * regional_mult, 2),
            "painting": round(painting_cost * regional_mult, 2),
            "flooring": round(flooring_cost * regional_mult, 2),
            "decoration": round(decoration_cost * regional_mult, 2),
            "lighting": round(lighting_cost * regional_mult, 2),
            "labor": round(labor_cost * regional_mult, 2),
            "total": round(total, 2),
            "currency": "USD",
            "region": region,
            "style_factor": style_mult,
        }

    def optimize_for_budget(
        self,
        furniture_items: list[dict],
        budget: float,
        room_area: float,
        style: str = "modern",
    ) -> dict:
        full_cost = self.calculate_full_cost(furniture_items, room_area, style)

        if full_cost["total"] <= budget:
            return {
                "status": "within_budget",
                "original_cost": full_cost["total"],
                "optimized_cost": full_cost["total"],
                "savings": 0,
                "suggestions": [],
                "items_kept": furniture_items,
                "items_removed": [],
            }

        sorted_items = sorted(
            furniture_items, key=lambda x: x.get("price", 0), reverse=True
        )
        kept = []
        removed = []
        running_total = full_cost["total"] - full_cost["furniture"]

        for item in sorted_items:
            if running_total + item["price"] <= budget:
                kept.append(item)
                running_total += item["price"]
            else:
                removed.append(item)

        suggestions = []
        if removed:
            suggestions.append(
                f"Remove {len(removed)} expensive items to fit budget"
            )
        suggestions.append("Consider phasing the renovation over multiple months")
        suggestions.append("Look for similar items at lower price points")

        return {
            "status": "optimized",
            "original_cost": full_cost["total"],
            "optimized_cost": round(running_total, 2),
            "savings": round(full_cost["total"] - running_total, 2),
            "suggestions": suggestions,
            "items_kept": kept,
            "items_removed": removed,
        }


cost_calculator = CostCalculator()
