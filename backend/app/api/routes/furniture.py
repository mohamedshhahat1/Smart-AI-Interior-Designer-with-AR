import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.request_models import FurnitureRecommendRequest
from backend.app.schemas.response_models import FurnitureRecommendation, FurnitureItem
from backend.app.services.recommendation_service import recommendation_service
from backend.app.services.ai_service import ai_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/furniture", tags=["Furniture"])


@router.post("/recommend", response_model=FurnitureRecommendation)
async def recommend_furniture(
    request: FurnitureRecommendRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Room).where(
            Room.id == uuid.UUID(request.room_id),
            Room.user_id == uuid.UUID(user_id),
        )
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    categories = request.categories
    if not categories and room.detected_objects:
        detected = room.detected_objects
        if isinstance(detected, list):
            categories = [obj.get("label", obj) if isinstance(obj, dict) else obj for obj in detected]
        elif isinstance(detected, dict):
            categories = list(detected.keys())

    if not categories:
        categories = ["sofa", "table", "lamp"]

    ai_recommendations = await ai_service.get_furniture_recommendations(
        detected_objects=room.detected_objects or {},
        style=request.style or "modern",
        budget=request.budget,
    )

    db_recommendations = await recommendation_service.get_recommendations(
        db=db,
        categories=categories,
        style=request.style,
        budget=request.budget,
    )

    all_items = ai_recommendations + db_recommendations
    seen_names = set()
    unique_items = []
    for item in all_items:
        name_key = item.get("name", "").lower()
        if name_key not in seen_names:
            seen_names.add(name_key)
            unique_items.append(item)

    total_cost = sum(item.get("price", 0) for item in unique_items)

    furniture_items = [
        FurnitureItem(
            id=item.get("id", ""),
            name=item.get("name", ""),
            category=item.get("category", ""),
            style=item.get("style"),
            price=item.get("price", 0),
            currency=item.get("currency", "USD"),
            image_url=item.get("image_url"),
            model_3d_url=item.get("model_3d_url"),
            rating=item.get("rating"),
        )
        for item in unique_items
    ]

    return FurnitureRecommendation(
        recommendations=furniture_items,
        total_cost=total_cost,
    )
