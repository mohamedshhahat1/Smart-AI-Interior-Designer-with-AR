import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    room_type: Mapped[str] = mapped_column(String(50), nullable=True)
    area: Mapped[float] = mapped_column(Float, nullable=True)
    dimensions: Mapped[dict] = mapped_column(JSON, nullable=True)
    detected_objects: Mapped[dict] = mapped_column(JSON, nullable=True)
    segmentation_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="rooms")
    designs = relationship("Design", back_populates="room", cascade="all, delete-orphan")
