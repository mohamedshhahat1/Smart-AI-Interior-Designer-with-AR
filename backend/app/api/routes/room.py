import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.response_models import RoomResponse, RoomAnalysis
from backend.app.services.ai_service import ai_service
from backend.app.core.security import get_current_user_id
from backend.app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/room", tags=["Room"])


@router.post("/upload", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def upload_room(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    if file.content_type not in settings.allowed_image_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image type: {file.content_type}",
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image exceeds {settings.max_upload_size_mb}MB limit",
        )

    image_filename = f"rooms/{user_id}/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    image_url = f"/storage/{image_filename}"

    analysis = await ai_service.analyze_room(image_url)

    room = Room(
        user_id=uuid.UUID(user_id),
        image_url=image_url,
        room_type=analysis.get("room_type"),
        area=analysis.get("area"),
        detected_objects=analysis.get("detected_objects"),
        segmentation_data=analysis.get("segmentation_data"),
    )
    db.add(room)
    await db.flush()

    return RoomResponse(
        id=str(room.id),
        user_id=str(room.user_id),
        image_url=room.image_url,
        room_type=room.room_type,
        area=room.area,
        detected_objects=room.detected_objects,
        created_at=room.created_at,
    )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Room).where(Room.id == uuid.UUID(room_id), Room.user_id == uuid.UUID(user_id))
    )
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    return RoomResponse(
        id=str(room.id),
        user_id=str(room.user_id),
        image_url=room.image_url,
        room_type=room.room_type,
        area=room.area,
        detected_objects=room.detected_objects,
        created_at=room.created_at,
    )


@router.get("/", response_model=list[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Room).where(Room.user_id == uuid.UUID(user_id)).order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()

    return [
        RoomResponse(
            id=str(room.id),
            user_id=str(room.user_id),
            image_url=room.image_url,
            room_type=room.room_type,
            area=room.area,
            detected_objects=room.detected_objects,
            created_at=room.created_at,
        )
        for room in rooms
    ]
