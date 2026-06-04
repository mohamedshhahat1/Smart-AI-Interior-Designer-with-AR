import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class Design(Base):
    __tablename__ = "designs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False, index=True
    )
    style: Mapped[str] = mapped_column(String(50), nullable=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    generated_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    color_palette: Mapped[dict] = mapped_column(JSON, nullable=True)
    furniture_list: Mapped[dict] = mapped_column(JSON, nullable=True)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    cost_breakdown: Mapped[dict] = mapped_column(JSON, nullable=True)
    ar_scene_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    room = relationship("Room", back_populates="designs")
