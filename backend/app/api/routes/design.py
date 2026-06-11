import uuid
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.models.design import Design
from backend.app.schemas.request_models import DesignGenerateRequest, DesignEnhanceRequest
from backend.app.schemas.response_models import DesignResponse
from backend.app.services.ai_service import ai_service
from backend.app.services.cost_service import cost_service
from backend.app.core.security import get_current_user_id
from backend.app.core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/design", tags=["Design"])


@router.post("/generate", response_model=DesignResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def generate_design(
    request: Request,
    body: DesignGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        rid = uuid.UUID(body.room_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    result = await db.execute(
        select(Room).where(Room.id == rid, Room.user_id == uuid.UUID(user_id))
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    room_analysis = {
        "room_type": room.room_type,
        "area": room.area,
        "detected_objects": room.detected_objects,
        "segmentation_data": room.segmentation_data,
        "image_url": room.image_url,
    }

    try:
        ai_result = await ai_service.generate_design(
            room_analysis=room_analysis,
            style=body.style,
            prompt=body.prompt,
            budget=body.budget,
            preserve_layout=body.preserve_layout,
        )
    except httpx.HTTPStatusError:
        logger.error("AI service returned error for design generation")
        raise HTTPException(status_code=502, detail="AI service unavailable")
    except httpx.RequestError as e:
        logger.error("AI service connection error: %s", e)
        raise HTTPException(status_code=503, detail="AI service not reachable")

    furniture_items = ai_result.get("furniture_list", [])
    cost_breakdown = cost_service.calculate_cost(
        furniture_items=furniture_items,
        room_area=room.area,
    )

    design = Design(
        room_id=room.id,
        style=body.style,
        prompt=body.prompt,
        generated_image_url=ai_result.get("image_url"),
        color_palette=ai_result.get("color_palette"),
        furniture_list=ai_result.get("furniture_list"),
        estimated_cost=cost_breakdown["total_cost"],
        cost_breakdown=cost_breakdown,
        ar_scene_data=ai_result.get("ar_scene_data"),
    )
    db.add(design)
    await db.flush()

    return _design_to_response(design)


@router.post("/enhance", response_model=DesignResponse)
@limiter.limit("20/minute")
async def enhance_design(
    request: Request,
    body: DesignEnhanceRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        did = uuid.UUID(body.design_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    result = await db.execute(select(Design).where(Design.id == did))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")

    room_result = await db.execute(
        select(Room).where(Room.id == design.room_id, Room.user_id == uuid.UUID(user_id))
    )
    if not room_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    design_data = {
        "image_url": design.generated_image_url,
        "style": design.style,
        "furniture_list": design.furniture_list,
        "color_palette": design.color_palette,
    }

    try:
        enhanced = await ai_service.enhance_design(design_data, body.instruction)
    except httpx.HTTPStatusError:
        logger.error("AI service returned error for design enhancement")
        raise HTTPException(status_code=502, detail="AI service unavailable")
    except httpx.RequestError as e:
        logger.error("AI service connection error: %s", e)
        raise HTTPException(status_code=503, detail="AI service not reachable")

    design.generated_image_url = enhanced.get("image_url", design.generated_image_url)
    design.furniture_list = enhanced.get("furniture_list", design.furniture_list)
    design.color_palette = enhanced.get("color_palette", design.color_palette)
    await db.flush()

    return _design_to_response(design)


@router.get("/", response_model=list[DesignResponse])
async def list_designs(
    room_id: str = None,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    query = (
        select(Design)
        .join(Room, Design.room_id == Room.id)
        .where(Room.user_id == uuid.UUID(user_id))
    )
    if room_id:
        query = query.where(Design.room_id == uuid.UUID(room_id))
    query = query.order_by(Design.created_at.desc())
    result = await db.execute(query)
    designs = result.scalars().all()
    return [_design_to_response(d) for d in designs]


@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        did = uuid.UUID(design_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    result = await db.execute(select(Design).where(Design.id == did))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")

    room_result = await db.execute(
        select(Room).where(Room.id == design.room_id, Room.user_id == uuid.UUID(user_id))
    )
    if not room_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return _design_to_response(design)


def _design_to_response(design: Design) -> DesignResponse:
    return DesignResponse(
        id=str(design.id),
        room_id=str(design.room_id),
        style=design.style or "modern",
        prompt=design.prompt,
        generated_image_url=design.generated_image_url,
        color_palette=design.color_palette,
        furniture_list=design.furniture_list or [],
        estimated_cost=design.estimated_cost or 0.0,
        cost_breakdown=design.cost_breakdown or {},
        created_at=design.created_at,
    )
