from typing import Optional


LABOR_RATES = {
    "installation": 50.0,
    "painting": 35.0,
    "flooring": 45.0,
    "electrical": 65.0,
    "plumbing": 70.0,
    "general": 40.0,
}

DECORATION_MULTIPLIER = {
    "paint": {"per_sqm": 8.0},
    "wallpaper": {"per_sqm": 15.0},
    "curtains": {"per_window": 120.0},
    "lighting_fixture": {"per_unit": 85.0},
}


class CostService:
    def calculate_cost(
        self,
        furniture_items: list[dict],
        room_area: Optional[float] = None,
        include_labor: bool = True,
        include_decoration: bool = True,
        window_count: int = 2,
        currency: str = "USD",
    ) -> dict:
        furniture_cost = sum(item.get("price", 0) for item in furniture_items)

        decoration_cost = 0.0
        if include_decoration and room_area:
            decoration_cost = (
                room_area * DECORATION_MULTIPLIER["paint"]["per_sqm"]
                + window_count * DECORATION_MULTIPLIER["curtains"]["per_window"]
                + 3 * DECORATION_MULTIPLIER["lighting_fixture"]["per_unit"]
            )

        lighting_cost = len(furniture_items) * 25.0

        flooring_cost = 0.0
        if room_area:
            flooring_cost = room_area * 30.0

        labor_cost = 0.0
        if include_labor:
            labor_hours = max(4, len(furniture_items) * 1.5)
            labor_cost = labor_hours * LABOR_RATES["installation"]
            if include_decoration and room_area:
                paint_hours = room_area * 0.3
                labor_cost += paint_hours * LABOR_RATES["painting"]

        total_cost = (
            furniture_cost + decoration_cost + lighting_cost + flooring_cost + labor_cost
        )

        return {
            "furniture_cost": round(furniture_cost, 2),
            "decoration_cost": round(decoration_cost, 2),
            "lighting_cost": round(lighting_cost, 2),
            "flooring_cost": round(flooring_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "total_cost": round(total_cost, 2),
            "currency": currency,
        }

    def get_budget_status(
        self, total_cost: float, budget: Optional[float] = None
    ) -> str:
        if budget is None:
            return "no_budget_set"
        if total_cost <= budget * 0.8:
            return "well_under_budget"
        if total_cost <= budget:
            return "within_budget"
        if total_cost <= budget * 1.1:
            return "slightly_over_budget"
        return "over_budget"

    def get_savings_suggestions(
        self, cost_breakdown: dict, budget: Optional[float] = None
    ) -> list[str]:
        suggestions = []
        if budget and cost_breakdown["total_cost"] > budget:
            overage = cost_breakdown["total_cost"] - budget
            suggestions.append(
                f"You are ${overage:.2f} over budget. Consider the following:"
            )
            if cost_breakdown["furniture_cost"] > budget * 0.5:
                suggestions.append(
                    "Consider more affordable furniture alternatives to reduce costs"
                )
            if cost_breakdown["flooring_cost"] > 0:
                suggestions.append(
                    "Keep existing flooring to save on material and labor costs"
                )
            if cost_breakdown["labor_cost"] > budget * 0.2:
                suggestions.append(
                    "DIY some installation tasks to reduce labor expenses"
                )
            suggestions.append(
                "Phase the renovation — prioritize high-impact items first"
            )
        return suggestions


cost_service = CostService()
