from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.request_models import (
    PetProfileCreateRequest,
    PetFriendlyAnalyzeRequest,
)
from backend.app.schemas.response_models import (
    PetProfileResponse,
    PetFriendlyAnalysisResponse,
    PetHazard,
    PetZone,
    PetMaterialRecommendation,
    PetProductRecommendation,
)
from backend.app.services.pet_friendly_service import pet_friendly_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/pet-friendly", tags=["Pet-Friendly Design"])


@router.post("/profiles", response_model=PetProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_pet_profile(
    request: PetProfileCreateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    profile = await pet_friendly_service.create_pet_profile(db, user_id, request.model_dump())
    return _profile_to_response(profile)


@router.get("/profiles", response_model=list[PetProfileResponse])
async def list_pet_profiles(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    profiles = await pet_friendly_service.get_pet_profiles(db, user_id)
    return [_profile_to_response(p) for p in profiles]


@router.get("/profiles/{profile_id}", response_model=PetProfileResponse)
async def get_pet_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    profile = await pet_friendly_service.get_pet_profile(db, profile_id)
    if not profile or str(profile.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet profile not found")
    return _profile_to_response(profile)


@router.post("/analyze", response_model=PetFriendlyAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_room(
    request: PetFriendlyAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        analysis = await pet_friendly_service.analyze_room(
            db=db, user_id=user_id,
            pet_profile_ids=request.pet_profile_ids,
            room_type=request.room_type,
            room_id=request.room_id,
            detected_objects=request.detected_objects,
            include_products=request.include_products,
            budget=request.budget,
        )
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _analysis_to_response(analysis)


@router.get("/analyses", response_model=list[PetFriendlyAnalysisResponse])
async def list_analyses(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    from sqlalchemy import select
    from backend.app.models.pet_friendly import PetFriendlyAnalysis
    import uuid

    result = await db.execute(
        select(PetFriendlyAnalysis)
        .where(PetFriendlyAnalysis.user_id == uuid.UUID(user_id))
        .order_by(PetFriendlyAnalysis.created_at.desc())
    )
    analyses = result.scalars().all()
    return [_analysis_to_response(a) for a in analyses]


def _profile_to_response(p) -> PetProfileResponse:
    return PetProfileResponse(
        id=str(p.id), name=p.name, species=p.species, breed=p.breed,
        size=p.size, age_years=p.age_years, weight_kg=p.weight_kg,
        energy_level=p.energy_level, is_indoor=p.is_indoor,
        is_destructive=p.is_destructive, sheds_fur=p.sheds_fur,
        climbs_furniture=p.climbs_furniture, has_allergies=p.has_allergies,
        special_needs=p.special_needs, created_at=p.created_at,
    )


def _analysis_to_response(a) -> PetFriendlyAnalysisResponse:
    hazards = [PetHazard(**h) for h in (a.hazards or [])]

    zones = [PetZone(**z) for z in (a.zone_plan or [])]

    materials = [PetMaterialRecommendation(**m) for m in (a.material_recommendations or [])]

    products = None
    if a.product_recommendations:
        products = [PetProductRecommendation(**p) for p in a.product_recommendations]

    interpretation = pet_friendly_service.get_score_interpretation(a.overall_score)

    return PetFriendlyAnalysisResponse(
        id=str(a.id), room_type=a.room_type,
        overall_score=a.overall_score, safety_score=a.safety_score,
        comfort_score=a.comfort_score, durability_score=a.durability_score,
        cleanliness_score=a.cleanliness_score,
        score_interpretation=interpretation,
        hazards=hazards, zone_plan=zones,
        material_recommendations=materials,
        plant_safety=a.plant_safety,
        cleaning_tips=a.cleaning_tips or [],
        product_recommendations=products,
        estimated_cost=a.estimated_cost,
        created_at=a.created_at,
    )
