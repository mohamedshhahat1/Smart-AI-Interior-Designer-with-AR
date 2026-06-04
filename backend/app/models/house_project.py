import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class HouseProject(Base):
    __tablename__ = "house_projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    style: Mapped[str] = mapped_column(String(50), nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    shared_theme: Mapped[dict] = mapped_column(JSON, nullable=True)
    color_palette: Mapped[dict] = mapped_column(JSON, nullable=True)
    material_palette: Mapped[dict] = mapped_column(JSON, nullable=True)
    lighting_scheme: Mapped[dict] = mapped_column(JSON, nullable=True)

    total_area: Mapped[float] = mapped_column(Float, nullable=True)
    room_count: Mapped[int] = mapped_column(Integer, default=0)
    total_estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    cost_breakdown_by_room: Mapped[dict] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(
        String(20), default="draft"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", backref="house_projects")
    room_designs = relationship(
        "HouseRoomDesign", back_populates="house_project", cascade="all, delete-orphan"
    )


class HouseRoomDesign(Base):
    __tablename__ = "house_room_designs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    house_project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("house_projects.id"), nullable=False, index=True
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=True
    )
    room_label: Mapped[str] = mapped_column(String(100), nullable=False)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    generated_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    room_color_palette: Mapped[dict] = mapped_column(JSON, nullable=True)
    furniture_list: Mapped[dict] = mapped_column(JSON, nullable=True)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    design_notes: Mapped[str] = mapped_column(Text, nullable=True)
    ar_scene_data: Mapped[dict] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    house_project = relationship("HouseProject", back_populates="room_designs")
    room = relationship("Room", backref="house_room_designs")
