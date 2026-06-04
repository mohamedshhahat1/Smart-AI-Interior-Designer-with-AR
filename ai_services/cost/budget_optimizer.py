from typing import Optional


class BudgetOptimizer:
    def allocate_budget(
        self,
        total_budget: float,
        room_type: str,
        priorities: Optional[list[str]] = None,
    ) -> dict:
        allocations = self._get_default_allocation(room_type)

        if priorities:
            allocations = self._adjust_for_priorities(allocations, priorities)

        result = {}
        for category, percentage in allocations.items():
            result[category] = {
                "percentage": round(percentage * 100, 1),
                "amount": round(total_budget * percentage, 2),
            }

        result["total_budget"] = total_budget
        return result

    def _get_default_allocation(self, room_type: str) -> dict:
        allocations = {
            "living_room": {
                "furniture": 0.45,
                "decoration": 0.15,
                "lighting": 0.10,
                "flooring": 0.15,
                "labor": 0.15,
            },
            "bedroom": {
                "furniture": 0.50,
                "decoration": 0.10,
                "lighting": 0.08,
                "flooring": 0.12,
                "labor": 0.20,
            },
            "kitchen": {
                "furniture": 0.35,
                "decoration": 0.10,
                "lighting": 0.10,
                "flooring": 0.20,
                "labor": 0.25,
            },
            "office": {
                "furniture": 0.55,
                "decoration": 0.05,
                "lighting": 0.15,
                "flooring": 0.10,
                "labor": 0.15,
            },
            "bathroom": {
                "furniture": 0.30,
                "decoration": 0.10,
                "lighting": 0.10,
                "flooring": 0.25,
                "labor": 0.25,
            },
        }
        return allocations.get(room_type, allocations["living_room"])

    def _adjust_for_priorities(
        self, allocations: dict, priorities: list[str]
    ) -> dict:
        adjusted = allocations.copy()
        boost = 0.05

        for priority in priorities:
            if priority in adjusted:
                adjusted[priority] += boost
                non_priority = [k for k in adjusted if k != priority]
                reduction = boost / len(non_priority)
                for key in non_priority:
                    adjusted[key] = max(0.05, adjusted[key] - reduction)

        total = sum(adjusted.values())
        return {k: v / total for k, v in adjusted.items()}

    def compare_scenarios(
        self, budget: float, scenarios: list[dict]
    ) -> list[dict]:
        results = []
        for scenario in scenarios:
            cost = sum(item.get("price", 0) for item in scenario.get("items", []))
            results.append({
                "name": scenario.get("name", "Unnamed"),
                "total_cost": round(cost, 2),
                "within_budget": cost <= budget,
                "remaining": round(budget - cost, 2),
                "utilization": round((cost / budget) * 100, 1) if budget > 0 else 0,
            })

        results.sort(key=lambda x: abs(x["remaining"]))
        return results


budget_optimizer = BudgetOptimizer()
