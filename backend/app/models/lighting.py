import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class LightingScene(Base):
    __tablename__ = "lighting_scenes"

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

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    activity: Mapped[str] = mapped_column(String(50), nullable=True)

    color_temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    brightness: Mapped[float] = mapped_column(Float, nullable=False)
    color_hex: Mapped[str] = mapped_column(String(7), nullable=True)
    saturation: Mapped[float] = mapped_column(Float, default=0.0)

    fixtures: Mapped[dict] = mapped_column(JSON, nullable=True)
    zones: Mapped[dict] = mapped_column(JSON, nullable=True)
    transition_duration: Mapped[float] = mapped_column(Float, default=2.0)

    is_circadian: Mapped[bool] = mapped_column(Boolean, default=False)
    circadian_schedule: Mapped[dict] = mapped_column(JSON, nullable=True)

    smart_home_config: Mapped[dict] = mapped_column(JSON, nullable=True)

    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="lighting_scenes")
    room = relationship("Room", backref="lighting_scenes")
    design = relationship("Design", backref="lighting_scenes")


class MoodProfile(Base):
    __tablename__ = "mood_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    mood_type: Mapped[str] = mapped_column(String(50), nullable=False)
    energy_level: Mapped[float] = mapped_column(Float, default=0.5)
    warmth_preference: Mapped[float] = mapped_column(Float, default=0.5)
    brightness_preference: Mapped[float] = mapped_column(Float, default=0.5)

    preferred_colors: Mapped[dict] = mapped_column(JSON, nullable=True)
    preferred_activities: Mapped[dict] = mapped_column(JSON, nullable=True)
    time_associations: Mapped[dict] = mapped_column(JSON, nullable=True)

    room_overrides: Mapped[dict] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="mood_profiles")


class LightingAnalytics(Base):
    __tablename__ = "lighting_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    scene_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lighting_scenes.id"), nullable=True
    )
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    time_of_day: Mapped[str] = mapped_column(String(20), nullable=False)
    duration_minutes: Mapped[float] = mapped_column(Float, nullable=True)
    feedback_rating: Mapped[int] = mapped_column(Integer, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="lighting_analytics")
    scene = relationship("LightingScene", backref="analytics")
