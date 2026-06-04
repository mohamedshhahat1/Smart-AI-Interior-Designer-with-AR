from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.furniture import Furniture


class RecommendationService:
    async def get_recommendations(
        self,
        db: AsyncSession,
        categories: list[str],
        style: Optional[str] = None,
        budget: Optional[float] = None,
        limit_per_category: int = 5,
    ) -> list[dict]:
        recommendations = []

        for category in categories:
            filters = [Furniture.category == category]
            if style:
                filters.append(Furniture.style == style)

            query = (
                select(Furniture)
                .where(and_(*filters))
                .order_by(Furniture.rating.desc().nullslast())
                .limit(limit_per_category)
            )
            result = await db.execute(query)
            items = result.scalars().all()

            for item in items:
                recommendations.append({
                    "id": str(item.id),
                    "name": item.name,
                    "category": item.category,
                    "style": item.style,
                    "price": item.price,
                    "currency": item.currency,
                    "image_url": item.image_url,
                    "model_3d_url": item.model_3d_url,
                    "rating": item.rating,
                    "dimensions": item.dimensions,
                })

        if budget:
            recommendations = self._filter_within_budget(recommendations, budget)

        return recommendations

    def _filter_within_budget(
        self, recommendations: list[dict], budget: float
    ) -> list[dict]:
        sorted_items = sorted(recommendations, key=lambda x: x.get("rating", 0) or 0, reverse=True)
        selected = []
        remaining_budget = budget

        for item in sorted_items:
            if item["price"] <= remaining_budget:
                selected.append(item)
                remaining_budget -= item["price"]

        return selected

    async def search_furniture(
        self,
        db: AsyncSession,
        query: str,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        limit: int = 20,
    ) -> list[dict]:
        filters = [Furniture.name.ilike(f"%{query}%")]
        if category:
            filters.append(Furniture.category == category)
        if max_price:
            filters.append(Furniture.price <= max_price)

        stmt = (
            select(Furniture)
            .where(and_(*filters))
            .order_by(Furniture.rating.desc().nullslast())
            .limit(limit)
        )
        result = await db.execute(stmt)
        items = result.scalars().all()

        return [
            {
                "id": str(item.id),
                "name": item.name,
                "category": item.category,
                "style": item.style,
                "price": item.price,
                "image_url": item.image_url,
                "rating": item.rating,
            }
            for item in items
        ]


recommendation_service = RecommendationService()
