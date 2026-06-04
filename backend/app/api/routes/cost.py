import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.models.design import Design
from backend.app.schemas.request_models import CostCalculateRequest
from backend.app.schemas.response_models import CostEstimationResponse, CostBreakdown
from backend.app.services.cost_service import cost_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/cost", tags=["Cost Estimation"])


@router.post("/calculate", response_model=CostEstimationResponse)
async def calculate_cost(
    request: CostCalculateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(select(Design).where(Design.id == uuid.UUID(request.design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")

    room_result = await db.execute(
        select(Room).where(Room.id == design.room_id, Room.user_id == uuid.UUID(user_id))
    )
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    furniture_items = design.furniture_list or []
    if isinstance(furniture_items, dict):
        furniture_items = list(furniture_items.values()) if furniture_items else []

    window_count = 2
    if room.detected_objects:
        objects = room.detected_objects
        if isinstance(objects, list):
            window_count = sum(
                1 for obj in objects
                if (isinstance(obj, dict) and obj.get("label") == "window")
                or obj == "window"
            )
        elif isinstance(objects, dict):
            window_count = objects.get("window_count", 2)

    breakdown = cost_service.calculate_cost(
        furniture_items=furniture_items,
        room_area=room.area,
        include_labor=request.include_labor,
        include_decoration=request.include_decoration,
        window_count=max(window_count, 1),
        currency=request.currency,
    )

    budget = design.estimated_cost
    budget_status = cost_service.get_budget_status(breakdown["total_cost"], budget)
    savings = cost_service.get_savings_suggestions(breakdown, budget)

    design.cost_breakdown = breakdown
    design.estimated_cost = breakdown["total_cost"]
    await db.flush()

    return CostEstimationResponse(
        design_id=str(design.id),
        breakdown=CostBreakdown(**breakdown),
        budget_status=budget_status,
        savings_suggestions=savings if savings else None,
    )
