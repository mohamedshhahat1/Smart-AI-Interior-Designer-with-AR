import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class PetProfile(Base):
    __tablename__ = "pet_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(20), nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=True)
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    age_years: Mapped[float] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=True)

    energy_level: Mapped[str] = mapped_column(String(20), default="medium")
    is_indoor: Mapped[bool] = mapped_column(Boolean, default=True)
    is_destructive: Mapped[bool] = mapped_column(Boolean, default=False)
    sheds_fur: Mapped[bool] = mapped_column(Boolean, default=True)
    climbs_furniture: Mapped[bool] = mapped_column(Boolean, default=False)
    has_allergies: Mapped[bool] = mapped_column(Boolean, default=False)

    special_needs: Mapped[dict] = mapped_column(JSON, nullable=True)
    behavioral_notes: Mapped[str] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="pet_profiles")


class PetFriendlyAnalysis(Base):
    __tablename__ = "pet_friendly_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=True
    )

    pet_profile_ids: Mapped[dict] = mapped_column(JSON, nullable=True)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)

    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False)
    comfort_score: Mapped[float] = mapped_column(Float, nullable=False)
    durability_score: Mapped[float] = mapped_column(Float, nullable=False)
    cleanliness_score: Mapped[float] = mapped_column(Float, nullable=False)

    hazards: Mapped[dict] = mapped_column(JSON, nullable=True)
    zone_plan: Mapped[dict] = mapped_column(JSON, nullable=True)
    material_recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)
    furniture_recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)
    plant_safety: Mapped[dict] = mapped_column(JSON, nullable=True)
    cleaning_tips: Mapped[dict] = mapped_column(JSON, nullable=True)
    product_recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)

    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="pet_friendly_analyses")
    room = relationship("Room", backref="pet_friendly_analyses")
