import uuid
from typing import Optional

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.lighting import LightingScene, MoodProfile, LightingAnalytics


class LightingService:
    async def save_scene(
        self,
        db: AsyncSession,
        user_id: str,
        scene_data: dict,
        name: str,
        mood: str,
        room_id: Optional[str] = None,
        design_id: Optional[str] = None,
        time_of_day: Optional[str] = None,
        activity: Optional[str] = None,
        is_circadian: bool = False,
        circadian_schedule: Optional[dict] = None,
    ) -> LightingScene:
        scene = LightingScene(
            user_id=uuid.UUID(user_id),
            room_id=uuid.UUID(room_id) if room_id else None,
            design_id=uuid.UUID(design_id) if design_id else None,
            name=name,
            mood=mood,
            time_of_day=time_of_day,
            activity=activity,
            color_temperature=scene_data.get("color_temperature", 3000),
            brightness=scene_data.get("brightness", 0.5),
            color_hex=scene_data.get("color_hex"),
            saturation=scene_data.get("saturation", 0.0),
            fixtures=scene_data.get("fixtures"),
            zones=scene_data.get("zones"),
            transition_duration=scene_data.get("transition_duration", 2.0),
            is_circadian=is_circadian,
            circadian_schedule=circadian_schedule,
        )
        db.add(scene)
        await db.flush()
        return scene

    async def get_user_scenes(
        self, db: AsyncSession, user_id: str, mood: Optional[str] = None
    ) -> list[LightingScene]:
        query = select(LightingScene).where(
            LightingScene.user_id == uuid.UUID(user_id)
        )
        if mood:
            query = query.where(LightingScene.mood == mood)
        query = query.order_by(LightingScene.created_at.desc())

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_scene(self, db: AsyncSession, scene_id: str) -> Optional[LightingScene]:
        result = await db.execute(
            select(LightingScene).where(LightingScene.id == uuid.UUID(scene_id))
        )
        return result.scalar_one_or_none()

    async def increment_usage(self, db: AsyncSession, scene: LightingScene):
        scene.usage_count += 1
        await db.flush()

    async def record_feedback(
        self,
        db: AsyncSession,
        user_id: str,
        scene_id: str,
        mood: str,
        rating: int,
        duration_minutes: Optional[float] = None,
    ):
        time_of_day = "unknown"
        scene = await self.get_scene(db, scene_id)
        if scene:
            time_of_day = scene.time_of_day or "unknown"
            await self.increment_usage(db, scene)

        analytics = LightingAnalytics(
            user_id=uuid.UUID(user_id),
            scene_id=uuid.UUID(scene_id),
            mood=mood,
            time_of_day=time_of_day,
            duration_minutes=duration_minutes,
            feedback_rating=rating,
        )
        db.add(analytics)
        await db.flush()

    async def get_insights(self, db: AsyncSession, user_id: str) -> dict:
        uid = uuid.UUID(user_id)

        scene_count = await db.execute(
            select(func.count(LightingScene.id)).where(LightingScene.user_id == uid)
        )
        total_scenes = scene_count.scalar() or 0

        mood_dist_result = await db.execute(
            select(LightingScene.mood, func.count(LightingScene.id))
            .where(LightingScene.user_id == uid)
            .group_by(LightingScene.mood)
        )
        mood_distribution = {row[0]: row[1] for row in mood_dist_result.all()}

        most_used = max(mood_distribution, key=mood_distribution.get) if mood_distribution else None

        avg_result = await db.execute(
            select(
                func.avg(LightingScene.brightness),
                func.avg(LightingScene.color_temperature),
            ).where(LightingScene.user_id == uid)
        )
        avg_row = avg_result.one_or_none()
        avg_brightness = round(float(avg_row[0]), 2) if avg_row and avg_row[0] else None
        avg_temp = int(avg_row[1]) if avg_row and avg_row[1] else None

        peak_result = await db.execute(
            select(LightingAnalytics.time_of_day, func.count(LightingAnalytics.id))
            .where(LightingAnalytics.user_id == uid)
            .group_by(LightingAnalytics.time_of_day)
            .order_by(func.count(LightingAnalytics.id).desc())
            .limit(1)
        )
        peak_row = peak_result.one_or_none()
        peak_time = peak_row[0] if peak_row else None

        recommendations = []
        if avg_brightness and avg_brightness > 0.7:
            recommendations.append("Consider dimmer scenes in the evening to support sleep quality")
        if avg_temp and avg_temp > 4500:
            recommendations.append("Your average color temperature is quite cool — try warmer tones after sunset")
        if total_scenes < 3:
            recommendations.append("Create more scenes for different moods to get personalized recommendations")
        if most_used == "focused":
            recommendations.append("You favor focus lighting — add a 'wind-down' scene for post-work transition")

        return {
            "total_scenes": total_scenes,
            "most_used_mood": most_used,
            "average_brightness": avg_brightness,
            "average_color_temperature": avg_temp,
            "peak_usage_time": peak_time,
            "mood_distribution": mood_distribution,
            "recommendations": recommendations,
        }

    async def save_mood_profile(
        self, db: AsyncSession, user_id: str, data: dict
    ) -> MoodProfile:
        profile = MoodProfile(
            user_id=uuid.UUID(user_id),
            name=data["name"],
            mood_type=data["mood_type"],
            energy_level=data.get("energy_level", 0.5),
            warmth_preference=data.get("warmth_preference", 0.5),
            brightness_preference=data.get("brightness_preference", 0.5),
            preferred_colors=data.get("preferred_colors"),
            preferred_activities=data.get("preferred_activities"),
        )
        db.add(profile)
        await db.flush()
        return profile

    async def get_mood_profiles(
        self, db: AsyncSession, user_id: str
    ) -> list[MoodProfile]:
        result = await db.execute(
            select(MoodProfile)
            .where(MoodProfile.user_id == uuid.UUID(user_id), MoodProfile.is_active == True)
            .order_by(MoodProfile.created_at.desc())
        )
        return list(result.scalars().all())


lighting_service = LightingService()
