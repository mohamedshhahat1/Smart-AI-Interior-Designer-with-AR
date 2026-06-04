"""Initial schema — all tables from migrations 001-007

Revision ID: 001
Revises:
Create Date: 2026-06-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_users_email", "users", ["email"])

    op.create_table(
        "rooms",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("image_url", sa.Text, nullable=False),
        sa.Column("room_type", sa.String(50)),
        sa.Column("area", sa.Float),
        sa.Column("dimensions", JSONB),
        sa.Column("detected_objects", JSONB),
        sa.Column("segmentation_data", JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_rooms_user_id", "rooms", ["user_id"])

    op.create_table(
        "designs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("room_id", UUID(as_uuid=True), sa.ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("style", sa.String(50)),
        sa.Column("prompt", sa.Text),
        sa.Column("generated_image_url", sa.Text),
        sa.Column("color_palette", JSONB),
        sa.Column("furniture_list", JSONB),
        sa.Column("estimated_cost", sa.Float),
        sa.Column("cost_breakdown", JSONB),
        sa.Column("ar_scene_data", JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_designs_room_id", "designs", ["room_id"])

    op.create_table(
        "furniture_catalog",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("style", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("currency", sa.String(3), server_default="USD"),
        sa.Column("dimensions", JSONB),
        sa.Column("color", sa.String(50)),
        sa.Column("material", sa.String(100)),
        sa.Column("image_url", sa.Text),
        sa.Column("model_3d_url", sa.Text),
        sa.Column("stock_quantity", sa.Integer, server_default="0"),
        sa.Column("rating", sa.Float),
        sa.Column("tags", JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("furniture_catalog")
    op.drop_table("designs")
    op.drop_table("rooms")
    op.drop_table("users")
