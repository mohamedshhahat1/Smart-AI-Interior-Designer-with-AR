import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.pet_friendly import PetProfile, PetFriendlyAnalysis
from backend.app.models.room import Room

from ai_services.pet_friendly.safety_analyzer import safety_analyzer
from ai_services.pet_friendly.zone_planner import zone_planner
from ai_services.pet_friendly.product_recommender import product_recommender


class PetFriendlyService:
    async def create_pet_profile(
        self, db: AsyncSession, user_id: str, data: dict
    ) -> PetProfile:
        profile = PetProfile(
            user_id=uuid.UUID(user_id),
            name=data["name"],
            species=data["species"],
            breed=data.get("breed"),
            size=data["size"],
            age_years=data.get("age_years"),
            weight_kg=data.get("weight_kg"),
            energy_level=data.get("energy_level", "medium"),
            is_indoor=data.get("is_indoor", True),
            is_destructive=data.get("is_destructive", False),
            sheds_fur=data.get("sheds_fur", True),
            climbs_furniture=data.get("climbs_furniture", False),
            has_allergies=data.get("has_allergies", False),
            special_needs=data.get("special_needs"),
            behavioral_notes=data.get("behavioral_notes"),
        )
        db.add(profile)
        await db.flush()
        return profile

    async def get_pet_profiles(
        self, db: AsyncSession, user_id: str
    ) -> list[PetProfile]:
        result = await db.execute(
            select(PetProfile)
            .where(PetProfile.user_id == uuid.UUID(user_id), PetProfile.is_active)
            .order_by(PetProfile.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_pet_profile(
        self, db: AsyncSession, profile_id: str
    ) -> Optional[PetProfile]:
        result = await db.execute(
            select(PetProfile).where(PetProfile.id == uuid.UUID(profile_id))
        )
        return result.scalar_one_or_none()

    async def analyze_room(
        self, db: AsyncSession, user_id: str,
        pet_profile_ids: list[str], room_type: str,
        room_id: Optional[str] = None,
        detected_objects: Optional[list[dict]] = None,
        include_products: bool = True,
        budget: Optional[float] = None,
    ) -> PetFriendlyAnalysis:
        pets = []
        for pid in pet_profile_ids:
            profile = await self.get_pet_profile(db, pid)
            if profile and str(profile.user_id) == user_id:
                pets.append({
                    "name": profile.name,
                    "species": profile.species,
                    "breed": profile.breed,
                    "size": profile.size,
                    "energy_level": profile.energy_level,
                    "is_indoor": profile.is_indoor,
                    "is_destructive": profile.is_destructive,
                    "sheds_fur": profile.sheds_fur,
                    "climbs_furniture": profile.climbs_furniture,
                    "has_allergies": profile.has_allergies,
                })

        if not pets:
            raise ValueError("No accessible pet profiles were provided")

        if room_id:
            result = await db.execute(
                select(Room).where(
                    Room.id == uuid.UUID(room_id),
                    Room.user_id == uuid.UUID(user_id),
                )
            )
            room = result.scalar_one_or_none()
            if not room:
                raise ValueError("Room not found")
            if not detected_objects and room.detected_objects:
                detected_objects = room.detected_objects if isinstance(room.detected_objects, list) else []
            if room.room_type:
                room_type = room.room_type

        safety_result = safety_analyzer.analyze(pets, room_type, detected_objects)
        zone_result = zone_planner.plan_zones(pets, room_type)

        products = None
        if include_products:
            products = product_recommender.recommend(pets, budget, room_type)

        overall = self._calculate_overall(
            safety_result["safety_score"],
            zone_result["comfort_score"],
            zone_result["durability_score"],
            zone_result["cleanliness_score"],
        )

        analysis = PetFriendlyAnalysis(
            user_id=uuid.UUID(user_id),
            room_id=uuid.UUID(room_id) if room_id else None,
            pet_profile_ids=pet_profile_ids,
            room_type=room_type,
            overall_score=overall,
            safety_score=safety_result["safety_score"],
            comfort_score=zone_result["comfort_score"],
            durability_score=zone_result["durability_score"],
            cleanliness_score=zone_result["cleanliness_score"],
            hazards=safety_result["hazards"],
            zone_plan=zone_result["zones"],
            material_recommendations=zone_result["materials"],
            plant_safety=safety_result["plant_safety"],
            cleaning_tips=zone_result["cleaning_tips"],
            product_recommendations=products,
            estimated_cost=zone_result["total_cost"],
        )
        db.add(analysis)
        await db.flush()
        return analysis

    def _calculate_overall(self, safety: float, comfort: float, durability: float, cleanliness: float) -> float:
        return round(safety * 0.35 + comfort * 0.25 + durability * 0.20 + cleanliness * 0.20, 1)

    def get_score_interpretation(self, score: float) -> str:
        if score >= 8.5:
            return "Excellent — your room is highly pet-friendly and safe"
        elif score >= 7.0:
            return "Good — pet-friendly with minor improvements possible"
        elif score >= 5.5:
            return "Fair — several changes recommended for pet safety and comfort"
        elif score >= 4.0:
            return "Needs Work — significant hazards or comfort issues detected"
        return "Unsafe — critical hazards present, address immediately"


pet_friendly_service = PetFriendlyService()
