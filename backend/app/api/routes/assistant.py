import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.request_models import AIAssistantRequest
from backend.app.schemas.response_models import AIAssistantResponse
from backend.app.services.ai_service import ai_service
from backend.app.core.security import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=AIAssistantResponse)
async def chat_with_assistant(
    request: AIAssistantRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    room_data = {}
    try:
        rid = uuid.UUID(request.room_id)
        result = await db.execute(
            select(Room).where(Room.id == rid, Room.user_id == uuid.UUID(user_id))
        )
        room = result.scalar_one_or_none()
        if room:
            room_data = {
                "room_type": room.room_type,
                "area": room.area,
                "detected_objects": room.detected_objects,
                "image_url": room.image_url,
            }
    except (ValueError, Exception) as e:
        logger.warning("Could not load room data: %s", e)

    try:
        ai_result = await ai_service.chat_with_assistant(
            room_data=room_data,
            message=request.message,
            conversation_history=request.conversation_history,
        )
    except Exception as e:
        logger.error("AI assistant error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI assistant service unavailable",
        )

    return AIAssistantResponse(
        message=ai_result.get("message", ""),
        suggestions=ai_result.get("suggestions", []),
    )
