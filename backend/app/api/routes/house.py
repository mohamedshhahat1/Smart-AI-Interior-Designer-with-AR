import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.db.database import get_db
from backend.app.models.house_project import HouseProject, HouseRoomDesign
from backend.app.models.room import Room
from backend.app.schemas.request_models import (
    HouseProjectCreateRequest,
    HouseProjectGenerateRequest,
    HouseProjectUpdateRequest,
    HouseRoomUpdateRequest,
)
from backend.app.schemas.response_models import (
    HouseProjectResponse,
    HouseProjectSummary,
    HouseRoomDesignResponse,
    HouseCostReport,
)
from backend.app.services.house_design_service import house_design_service
from backend.app.services.ai_service import ai_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/house", tags=["Multi-Room House Design"])


@router.post("/project", response_model=HouseProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_house_project(
    request: HouseProjectCreateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    validated_room_ids: dict[int, uuid.UUID] = {}
    for index, room_entry in enumerate(request.rooms):
        if not room_entry.room_id:
            continue
        try:
            room_id = uuid.UUID(room_entry.room_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid room ID for {room_entry.room_label}",
            ) from exc
        room_result = await db.execute(
            select(Room).where(
                Room.id == room_id,
                Room.user_id == uuid.UUID(user_id),
            )
        )
        if not room_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room not found for {room_entry.room_label}",
            )
        validated_room_ids[index] = room_id

    shared_theme = house_design_service.build_shared_theme(
        style=request.style,
        color_preferences=request.color_preferences,
        material_preferences=request.material_preferences,
        lighting_preference=request.lighting_preference,
    )

    project = HouseProject(
        user_id=uuid.UUID(user_id),
        name=request.name,
        description=request.description,
        style=request.style,
        budget=request.budget,
        currency=request.currency,
        shared_theme=shared_theme,
        color_palette={
            "primary": shared_theme["primary_colors"],
            "accent": shared_theme["accent_colors"],
        },
        material_palette={"materials": shared_theme["materials"]},
        lighting_scheme={"type": shared_theme["lighting"]},
        room_count=len(request.rooms),
        status="draft",
    )
    db.add(project)
    await db.flush()

    for i, room_entry in enumerate(request.rooms):
        room_design = HouseRoomDesign(
            house_project_id=project.id,
            room_id=validated_room_ids.get(i),
            room_label=room_entry.room_label,
            room_type=room_entry.room_type,
            order_index=i,
            status="pending",
        )
        db.add(room_design)

    await db.flush()

    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(HouseProject.id == project.id)
    )
    project = result.scalar_one()

    return _project_to_response(project)


@router.post("/project/{project_id}/generate", response_model=HouseProjectResponse)
async def generate_house_designs(
    project_id: str,
    request: HouseProjectGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(
            HouseProject.id == uuid.UUID(project_id),
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House project not found")

    if request.regenerate_rooms:
        for rd in project.room_designs:
            if str(rd.id) in request.regenerate_rooms:
                rd.status = "pending"

    project.status = "generating"
    await db.flush()

    await house_design_service.generate_all_room_designs(project, db)

    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(HouseProject.id == project.id)
    )
    project = result.scalar_one()

    return _project_to_response(project)


@router.get("/projects", response_model=list[HouseProjectSummary])
async def list_house_projects(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject)
        .where(HouseProject.user_id == uuid.UUID(user_id))
        .order_by(HouseProject.created_at.desc())
    )
    projects = result.scalars().all()

    return [
        HouseProjectSummary(
            id=str(p.id),
            name=p.name,
            style=p.style,
            room_count=p.room_count,
            total_estimated_cost=p.total_estimated_cost,
            status=p.status,
            created_at=p.created_at,
        )
        for p in projects
    ]


@router.get("/project/{project_id}", response_model=HouseProjectResponse)
async def get_house_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(
            HouseProject.id == uuid.UUID(project_id),
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House project not found")

    return _project_to_response(project)


@router.patch("/project/{project_id}", response_model=HouseProjectResponse)
async def update_house_project(
    project_id: str,
    request: HouseProjectUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(
            HouseProject.id == uuid.UUID(project_id),
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House project not found")

    if request.name:
        project.name = request.name
    if request.budget is not None:
        project.budget = request.budget
    if request.style:
        project.style = request.style
        project.shared_theme = house_design_service.build_shared_theme(
            style=request.style,
            color_preferences=request.color_preferences,
            lighting_preference=request.lighting_preference,
        )
    elif request.color_preferences or request.lighting_preference:
        project.shared_theme = house_design_service.build_shared_theme(
            style=project.style,
            color_preferences=request.color_preferences,
            lighting_preference=request.lighting_preference,
        )

    await db.flush()

    return _project_to_response(project)


@router.post("/room/refine", response_model=HouseRoomDesignResponse)
async def refine_room_design(
    request: HouseRoomUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseRoomDesign)
        .where(HouseRoomDesign.id == uuid.UUID(request.room_design_id))
    )
    room_design = result.scalar_one_or_none()
    if not room_design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room design not found")

    project_result = await db.execute(
        select(HouseProject).where(
            HouseProject.id == room_design.house_project_id,
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = project_result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    theme_context = (
        f"This room is part of a {project.style} house design. "
        f"Maintain visual consistency with the shared theme. "
    )
    full_instruction = theme_context + request.instruction

    design_data = {
        "image_url": room_design.generated_image_url,
        "style": project.style,
        "furniture_list": room_design.furniture_list,
        "color_palette": room_design.room_color_palette,
    }

    enhanced = await ai_service.enhance_design(design_data, full_instruction)

    room_design.generated_image_url = enhanced.get("image_url", room_design.generated_image_url)
    room_design.furniture_list = enhanced.get("furniture_list", room_design.furniture_list)
    room_design.design_notes = f"Refined: {request.instruction}"
    await db.flush()

    return _room_design_to_response(room_design)


@router.get("/room/{room_design_id}", response_model=HouseRoomDesignResponse)
async def get_house_room_design(
    room_design_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        parsed_id = uuid.UUID(room_design_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid house room design ID",
        ) from exc

    result = await db.execute(
        select(HouseRoomDesign)
        .join(HouseProject, HouseRoomDesign.house_project_id == HouseProject.id)
        .where(
            HouseRoomDesign.id == parsed_id,
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    room_design = result.scalar_one_or_none()
    if not room_design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="House room design not found",
        )
    return _room_design_to_response(room_design)


@router.get("/project/{project_id}/cost", response_model=HouseCostReport)
async def get_house_cost_report(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject)
        .options(selectinload(HouseProject.room_designs))
        .where(
            HouseProject.id == uuid.UUID(project_id),
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House project not found")

    report = house_design_service.generate_house_cost_report(project)
    return HouseCostReport(**report)


@router.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(HouseProject).where(
            HouseProject.id == uuid.UUID(project_id),
            HouseProject.user_id == uuid.UUID(user_id),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House project not found")

    await db.delete(project)


def _project_to_response(project: HouseProject) -> HouseProjectResponse:
    sorted_rooms = sorted(project.room_designs, key=lambda r: r.order_index)

    rooms = [
        _room_design_to_response(rd)
        for rd in sorted_rooms
    ]

    return HouseProjectResponse(
        id=str(project.id),
        user_id=str(project.user_id),
        name=project.name,
        description=project.description,
        style=project.style,
        budget=project.budget,
        currency=project.currency,
        shared_theme=project.shared_theme,
        color_palette=project.color_palette,
        material_palette=project.material_palette,
        lighting_scheme=project.lighting_scheme,
        total_area=project.total_area,
        room_count=project.room_count,
        total_estimated_cost=project.total_estimated_cost,
        cost_breakdown_by_room=project.cost_breakdown_by_room,
        status=project.status,
        rooms=rooms,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def _room_design_to_response(room_design: HouseRoomDesign) -> HouseRoomDesignResponse:
    return HouseRoomDesignResponse(
        id=str(room_design.id),
        room_label=room_design.room_label,
        room_type=room_design.room_type,
        order_index=room_design.order_index,
        room_id=str(room_design.room_id) if room_design.room_id else None,
        generated_image_url=room_design.generated_image_url,
        room_color_palette=room_design.room_color_palette,
        furniture_list=room_design.furniture_list,
        estimated_cost=room_design.estimated_cost,
        design_notes=room_design.design_notes,
        status=room_design.status,
        created_at=room_design.created_at,
    )
