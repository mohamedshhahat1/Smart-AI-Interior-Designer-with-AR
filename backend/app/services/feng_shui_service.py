import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.feng_shui import FengShuiAnalysis, FengShuiCure
from backend.app.models.room import Room

from ai_services.feng_shui.bagua_mapper import bagua_mapper
from ai_services.feng_shui.element_analyzer import element_analyzer
from ai_services.feng_shui.chi_flow_analyzer import chi_flow_analyzer
from ai_services.feng_shui.cure_recommender import cure_recommender


class FengShuiService:
    async def analyze_room(
        self,
        db: AsyncSession,
        user_id: str,
        room_type: str,
        room_id: Optional[str] = None,
        design_id: Optional[str] = None,
        compass_direction: Optional[str] = None,
        detected_objects: Optional[list[dict]] = None,
        room_dimensions: Optional[dict] = None,
        birth_year: Optional[int] = None,
        include_bagua: bool = True,
        include_element_analysis: bool = True,
    ) -> FengShuiAnalysis:
        if room_id and not detected_objects:
            result = await db.execute(select(Room).where(Room.id == uuid.UUID(room_id)))
            room = result.scalar_one_or_none()
            if room:
                detected_objects = room.detected_objects if isinstance(room.detected_objects, list) else []
                if room.room_type:
                    room_type = room.room_type

        bagua_data = None
        if include_bagua:
            bagua_data = bagua_mapper.map_room(
                room_type=room_type,
                compass_direction=compass_direction,
                detected_objects=detected_objects,
                room_dimensions=room_dimensions,
            )

        element_data = None
        element_balance_score = 7.0
        if include_element_analysis:
            element_data = element_analyzer.analyze(room_type, detected_objects)
            element_balance_score = element_analyzer.get_element_balance_score(element_data)

        chi_result = chi_flow_analyzer.analyze(
            room_type=room_type,
            detected_objects=detected_objects,
            room_dimensions=room_dimensions,
        )

        yin_yang_score = self._calculate_yin_yang_score(room_type, detected_objects)

        cures = cure_recommender.recommend_cures(
            chi_flow_issues=chi_result["issues"],
            element_analysis=element_data or [],
            room_type=room_type,
        )

        color_recs = cure_recommender.get_color_recommendations(room_type)
        furniture_advice = cure_recommender.get_furniture_placement_advice(room_type, detected_objects)

        lucky_directions = None
        birth_element = None
        if birth_year:
            kua_data = element_analyzer.calculate_kua_number(birth_year)
            lucky_directions = {
                "lucky": kua_data["lucky_directions"],
                "unlucky": kua_data["unlucky_directions"],
            }
            birth_element = kua_data["birth_element"]

        overall_score = self._calculate_overall_score(
            chi_flow=chi_result["chi_flow_score"],
            element_balance=element_balance_score,
            yin_yang=yin_yang_score,
            clutter=chi_result["clutter_score"],
            commanding=chi_result["commanding_position_score"],
        )

        analysis = FengShuiAnalysis(
            user_id=uuid.UUID(user_id),
            room_id=uuid.UUID(room_id) if room_id else None,
            design_id=uuid.UUID(design_id) if design_id else None,
            room_type=room_type,
            compass_direction=compass_direction,
            overall_score=overall_score,
            chi_flow_score=chi_result["chi_flow_score"],
            element_balance_score=element_balance_score,
            yin_yang_score=yin_yang_score,
            clutter_score=chi_result["clutter_score"],
            commanding_position_score=chi_result["commanding_position_score"],
            bagua_map=bagua_data,
            element_analysis=element_data,
            chi_flow_analysis={"issues": chi_result["issues"]},
            issues={"chi_flow": chi_result["issues"]},
            cures={"recommended": cures},
            furniture_placement=furniture_advice,
            color_recommendations=color_recs,
            lucky_directions=lucky_directions,
            birth_element=birth_element,
        )
        db.add(analysis)
        await db.flush()

        for cure_data in cures:
            cure = FengShuiCure(
                analysis_id=analysis.id,
                category=cure_data["category"],
                severity=cure_data["severity"],
                issue_description=cure_data["issue_description"],
                cure_description=cure_data["cure_description"],
                element=cure_data.get("element"),
                placement=cure_data.get("placement"),
                estimated_cost=cure_data.get("estimated_cost"),
                priority=cure_data.get("priority", 3),
            )
            db.add(cure)

        await db.flush()
        return analysis

    async def get_analysis(
        self, db: AsyncSession, analysis_id: str
    ) -> Optional[FengShuiAnalysis]:
        result = await db.execute(
            select(FengShuiAnalysis)
            .options(selectinload(FengShuiAnalysis.cure_items))
            .where(FengShuiAnalysis.id == uuid.UUID(analysis_id))
        )
        return result.scalar_one_or_none()

    async def get_user_analyses(
        self, db: AsyncSession, user_id: str
    ) -> list[FengShuiAnalysis]:
        result = await db.execute(
            select(FengShuiAnalysis)
            .options(selectinload(FengShuiAnalysis.cure_items))
            .where(FengShuiAnalysis.user_id == uuid.UUID(user_id))
            .order_by(FengShuiAnalysis.created_at.desc())
        )
        return list(result.scalars().all())

    async def apply_cure(
        self, db: AsyncSession, cure_id: str
    ) -> Optional[FengShuiCure]:
        result = await db.execute(
            select(FengShuiCure).where(FengShuiCure.id == uuid.UUID(cure_id))
        )
        cure = result.scalar_one_or_none()
        if cure:
            cure.is_applied = True
            await db.flush()
        return cure

    def get_compatibility(self, birth_year: int, room_type: str, compass_direction: Optional[str] = None) -> dict:
        kua_data = element_analyzer.calculate_kua_number(birth_year)

        room_recs = {}
        if compass_direction:
            is_lucky = compass_direction in kua_data["lucky_directions"]
            room_recs["direction_compatibility"] = "favorable" if is_lucky else "unfavorable"
            if not is_lucky:
                room_recs["suggestion"] = f"Your lucky directions are {', '.join(kua_data['lucky_directions'][:2])} — orient key furniture toward these"
            else:
                room_recs["suggestion"] = f"{compass_direction.capitalize()} is one of your lucky directions — excellent placement"

        room_recs["recommended_colors"] = kua_data["compatible_colors"]
        room_recs["compatible_elements"] = kua_data["compatible_elements"]
        room_recs["room_type"] = room_type

        return {
            "birth_year": birth_year,
            "kua_number": kua_data["kua_number"],
            "birth_element": kua_data["birth_element"],
            "lucky_directions": kua_data["lucky_directions"],
            "unlucky_directions": kua_data["unlucky_directions"],
            "compatible_colors": kua_data["compatible_colors"],
            "compatible_elements": kua_data["compatible_elements"],
            "room_recommendations": room_recs,
        }

    def _calculate_yin_yang_score(
        self, room_type: str, detected_objects: Optional[list[dict]]
    ) -> float:
        ideal_balance = {
            "bedroom": 0.35,
            "office": 0.65,
            "living_room": 0.55,
            "kitchen": 0.60,
            "bathroom": 0.40,
            "dining_room": 0.55,
        }
        ideal_yang = ideal_balance.get(room_type, 0.50)

        if not detected_objects:
            return 7.0

        yang_items = {"tv", "lamp", "desk", "oven", "mirror", "clock"}
        yin_items = {"bed", "sofa", "rug", "curtain", "plant", "cushion"}

        yang_count = 0
        yin_count = 0
        for obj in detected_objects:
            label = (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()
            if label in yang_items:
                yang_count += 1
            elif label in yin_items:
                yin_count += 1

        total = yang_count + yin_count
        if total == 0:
            return 7.0

        actual_yang = yang_count / total
        deviation = abs(actual_yang - ideal_yang)
        score = max(1.0, 10.0 - deviation * 15)
        return round(score, 1)

    def _calculate_overall_score(
        self, chi_flow: float, element_balance: float, yin_yang: float,
        clutter: float, commanding: float,
    ) -> float:
        weighted = (
            chi_flow * 0.25
            + element_balance * 0.20
            + yin_yang * 0.15
            + clutter * 0.20
            + commanding * 0.20
        )
        return round(weighted, 1)

    def get_score_interpretation(self, score: float) -> str:
        if score >= 8.5:
            return "Excellent Feng Shui — your space has harmonious energy flow, balanced elements, and strong commanding positions"
        elif score >= 7.0:
            return "Good Feng Shui — your space has positive energy with minor areas for improvement"
        elif score >= 5.5:
            return "Fair Feng Shui — several areas need attention to improve energy flow and balance"
        elif score >= 4.0:
            return "Needs Improvement — significant Feng Shui issues are affecting the room's energy"
        else:
            return "Poor Feng Shui — major adjustments needed to restore harmony and positive chi flow"


feng_shui_service = FengShuiService()
