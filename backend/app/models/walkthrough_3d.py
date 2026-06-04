import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class Room3DModel(Base):
    __tablename__ = "room_3d_models"

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

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)

    room_geometry: Mapped[dict] = mapped_column(JSON, nullable=True)
    depth_map_url: Mapped[str] = mapped_column(Text, nullable=True)
    mesh_url: Mapped[str] = mapped_column(Text, nullable=True)
    texture_urls: Mapped[dict] = mapped_column(JSON, nullable=True)
    glb_model_url: Mapped[str] = mapped_column(Text, nullable=True)
    usdz_model_url: Mapped[str] = mapped_column(Text, nullable=True)

    furniture_3d_objects: Mapped[dict] = mapped_column(JSON, nullable=True)
    lighting_setup: Mapped[dict] = mapped_column(JSON, nullable=True)
    camera_positions: Mapped[dict] = mapped_column(JSON, nullable=True)
    walkthrough_path: Mapped[dict] = mapped_column(JSON, nullable=True)

    dimensions: Mapped[dict] = mapped_column(JSON, nullable=True)
    reconstruction_method: Mapped[str] = mapped_column(String(50), default="depth_estimation")
    quality_level: Mapped[str] = mapped_column(String(20), default="standard")
    polygon_count: Mapped[int] = mapped_column(Integer, nullable=True)
    file_size_mb: Mapped[float] = mapped_column(Float, nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="pending")
    processing_time_seconds: Mapped[float] = mapped_column(Float, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="room_3d_models")
    room = relationship("Room", backref="room_3d_models")
    design = relationship("Design", backref="room_3d_models")


class WalkthroughSession(Base):
    __tablename__ = "walkthrough_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("room_3d_models.id"), nullable=False, index=True
    )

    camera_path_taken: Mapped[dict] = mapped_column(JSON, nullable=True)
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=True)
    screenshots_taken: Mapped[int] = mapped_column(Integer, default=0)
    annotations: Mapped[dict] = mapped_column(JSON, nullable=True)
    comparison_model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="walkthrough_sessions")
    model = relationship("Room3DModel", backref="walkthrough_sessions")
