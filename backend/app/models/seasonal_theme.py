import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON, Integer, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class SeasonalTheme(Base):
    __tablename__ = "seasonal_themes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=True
    )
    design_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("designs.id"), nullable=True
    )

    theme_type: Mapped[str] = mapped_column(String(20), nullable=False)
    season: Mapped[str] = mapped_column(String(20), nullable=True)
    holiday: Mapped[str] = mapped_column(String(50), nullable=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    color_palette: Mapped[dict] = mapped_column(JSON, nullable=True)
    textures: Mapped[dict] = mapped_column(JSON, nullable=True)
    materials: Mapped[dict] = mapped_column(JSON, nullable=True)
    lighting_mood: Mapped[str] = mapped_column(String(50), nullable=True)

    decor_items: Mapped[dict] = mapped_column(JSON, nullable=True)
    diy_projects: Mapped[dict] = mapped_column(JSON, nullable=True)
    scent_recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)
    music_playlist_mood: Mapped[str] = mapped_column(String(50), nullable=True)

    generated_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    ar_overlay_data: Mapped[dict] = mapped_column(JSON, nullable=True)

    budget_tier: Mapped[str] = mapped_column(String(20), default="medium")
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    reusability_score: Mapped[float] = mapped_column(Float, nullable=True)

    transition_from: Mapped[str] = mapped_column(String(50), nullable=True)
    transition_tips: Mapped[dict] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="seasonal_themes")
    room = relationship("Room", backref="seasonal_themes")
    design = relationship("Design", backref="seasonal_themes")
