import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Text, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.db.database import Base


class FengShuiAnalysis(Base):
    __tablename__ = "feng_shui_analyses"

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

    room_type: Mapped[str] = mapped_column(String(50), nullable=False)
    compass_direction: Mapped[str] = mapped_column(String(20), nullable=True)

    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    chi_flow_score: Mapped[float] = mapped_column(Float, nullable=False)
    element_balance_score: Mapped[float] = mapped_column(Float, nullable=False)
    yin_yang_score: Mapped[float] = mapped_column(Float, nullable=False)
    clutter_score: Mapped[float] = mapped_column(Float, nullable=False)
    commanding_position_score: Mapped[float] = mapped_column(Float, nullable=False)

    bagua_map: Mapped[dict] = mapped_column(JSON, nullable=True)
    element_analysis: Mapped[dict] = mapped_column(JSON, nullable=True)
    chi_flow_analysis: Mapped[dict] = mapped_column(JSON, nullable=True)

    issues: Mapped[dict] = mapped_column(JSON, nullable=True)
    cures: Mapped[dict] = mapped_column(JSON, nullable=True)
    enhancements: Mapped[dict] = mapped_column(JSON, nullable=True)

    furniture_placement: Mapped[dict] = mapped_column(JSON, nullable=True)
    color_recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)

    lucky_directions: Mapped[dict] = mapped_column(JSON, nullable=True)
    birth_element: Mapped[str] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="feng_shui_analyses")
    room = relationship("Room", backref="feng_shui_analyses")
    design = relationship("Design", backref="feng_shui_analyses")


class FengShuiCure(Base):
    __tablename__ = "feng_shui_cures"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("feng_shui_analyses.id"), nullable=False, index=True
    )

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    issue_description: Mapped[str] = mapped_column(Text, nullable=False)
    cure_description: Mapped[str] = mapped_column(Text, nullable=False)
    element: Mapped[str] = mapped_column(String(20), nullable=True)
    placement: Mapped[str] = mapped_column(String(100), nullable=True)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=3)
    is_applied: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    analysis = relationship("FengShuiAnalysis", backref="cure_items")
