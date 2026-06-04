import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.seasonal_theme import SeasonalTheme

from ai_services.seasonal.season_detector import season_detector
from ai_services.seasonal.theme_generator import theme_generator


class SeasonalService:
    def detect_season(
        self, hemisphere: str = "northern", days_ahead: int = 30
    ) -> dict:
        return season_detector.detect(hemisphere=hemisphere, days_ahead=days_ahead)

    def generate_theme(
        self,
        theme_type: str,
        season: Optional[str] = None,
        holiday: Optional[str] = None,
        room_type: str = "living_room",
        budget_tier: str = "medium",
        intensity: float = 0.7,
        base_style: Optional[str] = None,
        include_diy: bool = True,
        include_scents: bool = True,
    ) -> dict:
        return theme_generator.generate(
            theme_type=theme_type, season=season, holiday=holiday,
            room_type=room_type, budget_tier=budget_tier, intensity=intensity,
            base_style=base_style, include_diy=include_diy, include_scents=include_scents,
        )

    def generate_transition(
        self,
        from_theme: Optional[dict] = None,
        to_season: Optional[str] = None,
        to_holiday: Optional[str] = None,
        gradual: bool = True,
    ) -> dict:
        return theme_generator.generate_transition(
            from_theme=from_theme, to_season=to_season,
            to_holiday=to_holiday, gradual=gradual,
        )

    async def save_theme(
        self, db: AsyncSession, user_id: str, theme_data: dict,
        room_id: Optional[str] = None, design_id: Optional[str] = None,
    ) -> SeasonalTheme:
        theme = SeasonalTheme(
            user_id=uuid.UUID(user_id),
            room_id=uuid.UUID(room_id) if room_id else None,
            design_id=uuid.UUID(design_id) if design_id else None,
            theme_type=theme_data.get("theme_type", "season"),
            season=theme_data.get("season"),
            holiday=theme_data.get("holiday"),
            name=theme_data.get("name", "Untitled Theme"),
            description=theme_data.get("description"),
            color_palette=theme_data.get("color_palette"),
            textures=theme_data.get("textures"),
            materials=theme_data.get("materials"),
            lighting_mood=theme_data.get("lighting_mood"),
            decor_items=theme_data.get("decor_items"),
            diy_projects=theme_data.get("diy_projects"),
            scent_recommendations=theme_data.get("scent_recommendations"),
            music_playlist_mood=theme_data.get("music_playlist_mood"),
            budget_tier=theme_data.get("budget_tier", "medium"),
            estimated_cost=theme_data.get("estimated_cost"),
            reusability_score=theme_data.get("reusability_score"),
        )
        db.add(theme)
        await db.flush()
        return theme

    async def get_user_themes(
        self, db: AsyncSession, user_id: str,
        theme_type: Optional[str] = None,
    ) -> list[SeasonalTheme]:
        query = select(SeasonalTheme).where(
            SeasonalTheme.user_id == uuid.UUID(user_id)
        )
        if theme_type:
            query = query.where(SeasonalTheme.theme_type == theme_type)
        query = query.order_by(SeasonalTheme.created_at.desc())

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_theme(self, db: AsyncSession, theme_id: str) -> Optional[SeasonalTheme]:
        result = await db.execute(
            select(SeasonalTheme).where(SeasonalTheme.id == uuid.UUID(theme_id))
        )
        return result.scalar_one_or_none()

    async def toggle_favorite(self, db: AsyncSession, theme: SeasonalTheme) -> SeasonalTheme:
        theme.is_favorite = not theme.is_favorite
        await db.flush()
        return theme

    async def delete_theme(self, db: AsyncSession, theme: SeasonalTheme):
        await db.delete(theme)


seasonal_service = SeasonalService()
