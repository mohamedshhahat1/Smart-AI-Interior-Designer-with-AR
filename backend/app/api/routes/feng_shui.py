import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.request_models import (
    FengShuiAnalyzeRequest,
    FengShuiApplyCureRequest,
    FengShuiCompatibilityRequest,
)
from backend.app.schemas.response_models import (
    FengShuiAnalysisResponse,
    FengShuiCureResponse,
    FengShuiCompatibilityResponse,
    BaguaZone,
    ElementBalance,
    ChiFlowIssue,
    FurniturePlacementAdvice,
)
from backend.app.services.feng_shui_service import feng_shui_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/feng-shui", tags=["Feng Shui Analysis"])


@router.post("/analyze", response_model=FengShuiAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_feng_shui(
    request: FengShuiAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    analysis = await feng_shui_service.analyze_room(
        db=db,
        user_id=user_id,
        room_type=request.room_type,
        room_id=request.room_id,
        design_id=request.design_id,
        compass_direction=request.compass_direction,
        detected_objects=request.detected_objects,
        room_dimensions=request.room_dimensions,
        birth_year=request.birth_year,
        include_bagua=request.include_bagua,
        include_element_analysis=request.include_element_analysis,
    )

    return _analysis_to_response(analysis)


@router.get("/analyses", response_model=list[FengShuiAnalysisResponse])
async def list_analyses(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    analyses = await feng_shui_service.get_user_analyses(db, user_id)
    return [_analysis_to_response(a) for a in analyses]


@router.get("/analyses/{analysis_id}", response_model=FengShuiAnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    analysis = await feng_shui_service.get_analysis(db, analysis_id)
    if not analysis or str(analysis.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return _analysis_to_response(analysis)


@router.post("/cures/apply")
async def apply_cure(
    request: FengShuiApplyCureRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    analysis = await feng_shui_service.get_analysis(db, request.analysis_id)
    if not analysis or str(analysis.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    cure = await feng_shui_service.apply_cure(db, request.cure_id)
    if not cure:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cure not found")

    return {"status": "applied", "cure_id": str(cure.id), "cure_description": cure.cure_description}


@router.post("/compatibility", response_model=FengShuiCompatibilityResponse)
async def check_compatibility(
    request: FengShuiCompatibilityRequest,
    user_id: str = Depends(get_current_user_id),
):
    result = feng_shui_service.get_compatibility(
        birth_year=request.birth_year,
        room_type=request.room_type,
        compass_direction=request.compass_direction,
    )
    return FengShuiCompatibilityResponse(**result)


def _analysis_to_response(analysis) -> FengShuiAnalysisResponse:
    bagua_zones = None
    if analysis.bagua_map:
        bagua_zones = [BaguaZone(**z) for z in analysis.bagua_map]

    element_data = None
    if analysis.element_analysis:
        element_data = [ElementBalance(**e) for e in analysis.element_analysis]

    chi_issues = None
    if analysis.chi_flow_analysis and analysis.chi_flow_analysis.get("issues"):
        chi_issues = [ChiFlowIssue(**i) for i in analysis.chi_flow_analysis["issues"]]

    cures = []
    if hasattr(analysis, "cure_items") and analysis.cure_items:
        cures = [
            FengShuiCureResponse(
                id=str(c.id), category=c.category, severity=c.severity,
                issue_description=c.issue_description, cure_description=c.cure_description,
                element=c.element, placement=c.placement, estimated_cost=c.estimated_cost,
                priority=c.priority, is_applied=c.is_applied,
            )
            for c in sorted(analysis.cure_items, key=lambda x: x.priority)
        ]
    elif analysis.cures and analysis.cures.get("recommended"):
        cures = [
            FengShuiCureResponse(
                id="pending", category=c["category"], severity=c["severity"],
                issue_description=c["issue_description"], cure_description=c["cure_description"],
                element=c.get("element"), placement=c.get("placement"),
                estimated_cost=c.get("estimated_cost"), priority=c.get("priority", 3),
                is_applied=False,
            )
            for c in analysis.cures["recommended"]
        ]

    furniture = None
    if analysis.furniture_placement:
        furniture = [FurniturePlacementAdvice(**f) for f in analysis.furniture_placement]

    interpretation = feng_shui_service.get_score_interpretation(analysis.overall_score)

    return FengShuiAnalysisResponse(
        id=str(analysis.id),
        room_type=analysis.room_type,
        compass_direction=analysis.compass_direction,
        overall_score=analysis.overall_score,
        chi_flow_score=analysis.chi_flow_score,
        element_balance_score=analysis.element_balance_score,
        yin_yang_score=analysis.yin_yang_score,
        clutter_score=analysis.clutter_score,
        commanding_position_score=analysis.commanding_position_score,
        score_interpretation=interpretation,
        bagua_map=bagua_zones,
        element_analysis=element_data,
        chi_flow_issues=chi_issues,
        cures=cures,
        furniture_placement=furniture,
        color_recommendations=analysis.color_recommendations,
        lucky_directions=analysis.lucky_directions,
        birth_element=analysis.birth_element,
        summary=interpretation,
        created_at=analysis.created_at,
    )
