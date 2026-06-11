import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.design import Design
from backend.app.models.house_project import HouseProject, HouseRoomDesign
from backend.app.models.room import Room
from backend.app.schemas.request_models import ARSceneRequest
from backend.app.schemas.response_models import ARSceneResponse
from backend.app.services.ar_service import ar_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/ar", tags=["Augmented Reality"])


@router.post("/generate-scene", response_model=ARSceneResponse)
async def generate_ar_scene(
    request: ARSceneRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    if bool(request.design_id) == bool(request.house_room_design_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide exactly one design source",
        )

    source_id: uuid.UUID
    furniture_data = None

    if request.design_id:
        try:
            source_id = uuid.UUID(request.design_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid design ID",
            ) from exc

        result = await db.execute(select(Design).where(Design.id == source_id))
        design = result.scalar_one_or_none()
        if not design:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Design not found"
            )

        room_result = await db.execute(
            select(Room).where(
                Room.id == design.room_id, Room.user_id == uuid.UUID(user_id)
            )
        )
        if not room_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        furniture_data = design.furniture_list
    else:
        try:
            source_id = uuid.UUID(request.house_room_design_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid house room design ID",
            ) from exc

        result = await db.execute(
            select(HouseRoomDesign)
            .join(HouseProject, HouseRoomDesign.house_project_id == HouseProject.id)
            .where(
                HouseRoomDesign.id == source_id,
                HouseProject.user_id == uuid.UUID(user_id),
            )
        )
        house_room = result.scalar_one_or_none()
        if not house_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="House room design not found",
            )
        furniture_data = house_room.furniture_list

    furniture_list = []
    if furniture_data:
        if isinstance(furniture_data, list):
            furniture_list = furniture_data
        elif isinstance(furniture_data, dict):
            for key, value in furniture_data.items():
                item = {"name": key}
                if isinstance(value, dict):
                    item.update(value)
                furniture_list.append(item)

    scene_data = ar_service.generate_ar_scene(
        furniture_list=furniture_list,
        room_dimensions=request.room_dimensions,
    )

    return ARSceneResponse(
        design_id=str(source_id),
        scene_objects=scene_data["scene_objects"],
        room_anchor=scene_data["room_anchor"],
        lighting_config=scene_data["lighting_config"],
    )
