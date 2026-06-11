import uuid
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.response_models import RoomResponse, RoomAnalysis
from backend.app.services.ai_service import ai_service
from backend.app.services.storage_service import storage_service
from backend.app.core.security import get_current_user_id
from backend.app.core.config import get_settings
from backend.app.core.limiter import limiter

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/room", tags=["Room"])


@router.post("/upload", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def upload_room(
    request: Request,
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

    ext = file.filename.split('.')[-1] if file.filename and '.' in file.filename else 'jpg'
    image_filename = f"rooms/{user_id}/{uuid.uuid4()}.{ext}"

    storage_service.upload_bytes(image_filename, contents, content_type=file.content_type or "image/jpeg")
    # Stored URL is the internal endpoint so the AI service can fetch it inside
    # the docker network. Client responses convert it to the public endpoint.
    image_url = storage_service.get_internal_url(image_filename)

    try:
        analysis = await ai_service.analyze_room(image_url)
    except httpx.HTTPStatusError:
        logger.error("AI service returned error for room analysis")
        raise HTTPException(status_code=502, detail="AI service unavailable")
    except httpx.RequestError as e:
        logger.error("AI service connection error: %s", e)
        raise HTTPException(status_code=503, detail="AI service not reachable")

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

    return _room_to_response(room)


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        rid = uuid.UUID(room_id)
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    result = await db.execute(
        select(Room).where(Room.id == rid, Room.user_id == uid)
    )
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    return _room_to_response(room)


@router.get("/", response_model=list[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Room).where(Room.user_id == uuid.UUID(user_id)).order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()

    return [_room_to_response(room) for room in rooms]


def _room_to_response(room: Room) -> RoomResponse:
    return RoomResponse(
        id=str(room.id),
        user_id=str(room.user_id),
        image_url=storage_service.to_public_url(room.image_url),
        room_type=room.room_type or "unknown",
        area=room.area,
        detected_objects=room.detected_objects or [],
        created_at=room.created_at,
    )
