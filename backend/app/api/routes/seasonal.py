import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.request_models import (
    SeasonalThemeGenerateRequest,
    SeasonalTransitionRequest,
    AutoSeasonDetectRequest,
)
from backend.app.schemas.response_models import (
    SeasonalThemeResponse,
    SeasonDetectResponse,
    SeasonalTransitionResponse,
    DecorItem,
    DIYProject,
    ScentRecommendation,
)
from backend.app.services.seasonal_service import seasonal_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/seasonal", tags=["Seasonal & Holiday Themes"])


@router.post("/detect", response_model=SeasonDetectResponse)
async def detect_current_season(
    request: AutoSeasonDetectRequest,
    user_id: str = Depends(get_current_user_id),
):
    result = seasonal_service.detect_season(
        hemisphere=request.hemisphere,
        days_ahead=request.days_ahead,
    )
    return SeasonDetectResponse(**result)


@router.post("/generate", response_model=SeasonalThemeResponse, status_code=status.HTTP_201_CREATED)
async def generate_seasonal_theme(
    request: SeasonalThemeGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    room_type = request.room_type
    if request.room_id:
        try:
            parsed_room_id = uuid.UUID(request.room_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid room ID",
            ) from exc
        result = await db.execute(
            select(Room).where(
                Room.id == parsed_room_id,
                Room.user_id == uuid.UUID(user_id),
            )
        )
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found",
            )
        room_type = room.room_type or room_type

    theme_data = seasonal_service.generate_theme(
        theme_type=request.theme_type,
        season=request.season,
        holiday=request.holiday,
        room_type=room_type,
        budget_tier=request.budget_tier,
        intensity=request.intensity,
        base_style=request.base_style,
        include_diy=request.include_diy,
        include_scents=request.include_scents,
    )

    saved = await seasonal_service.save_theme(
        db=db, user_id=user_id, theme_data=theme_data,
        room_id=request.room_id, design_id=request.design_id,
    )

    return _theme_to_response(saved, theme_data)


@router.post("/transition", response_model=SeasonalTransitionResponse)
async def plan_transition(
    request: SeasonalTransitionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    from_theme = None
    if request.from_theme_id:
        saved = await seasonal_service.get_theme(db, request.from_theme_id)
        if saved and str(saved.user_id) == user_id:
            from_theme = {
                "name": saved.name,
                "decor_items": saved.decor_items or [],
            }

    result = seasonal_service.generate_transition(
        from_theme=from_theme,
        to_season=request.to_season,
        to_holiday=request.to_holiday,
        gradual=request.gradual,
    )
    return SeasonalTransitionResponse(**result)


@router.get("/themes", response_model=list[SeasonalThemeResponse])
async def list_themes(
    theme_type: str = None,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    themes = await seasonal_service.get_user_themes(db, user_id, theme_type)
    return [_theme_to_response(t) for t in themes]


@router.get("/themes/{theme_id}", response_model=SeasonalThemeResponse)
async def get_theme(
    theme_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    theme = await seasonal_service.get_theme(db, theme_id)
    if not theme or str(theme.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")
    return _theme_to_response(theme)


@router.post("/themes/{theme_id}/favorite")
async def toggle_favorite(
    theme_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    theme = await seasonal_service.get_theme(db, theme_id)
    if not theme or str(theme.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")
    updated = await seasonal_service.toggle_favorite(db, theme)
    return {"is_favorite": updated.is_favorite}


@router.delete("/themes/{theme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_theme(
    theme_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    theme = await seasonal_service.get_theme(db, theme_id)
    if not theme or str(theme.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")
    await seasonal_service.delete_theme(db, theme)


def _theme_to_response(theme, extra_data: dict = None) -> SeasonalThemeResponse:
    data = extra_data or {}

    decor_items = None
    raw_decor = data.get("decor_items") or (theme.decor_items if hasattr(theme, "decor_items") else None)
    if raw_decor and isinstance(raw_decor, list):
        decor_items = [
            DecorItem(
                name=d.get("name", ""),
                category=d.get("category", "general"),
                placement=d.get("placement", ""),
                estimated_cost=d.get("estimated_cost"),
                reusable=d.get("reusable", True),
                diy_possible=d.get("diy_possible", False),
            )
            for d in raw_decor
        ]

    diy_projects = None
    raw_diy = data.get("diy_projects") or (theme.diy_projects if hasattr(theme, "diy_projects") else None)
    if raw_diy and isinstance(raw_diy, list):
        diy_projects = [
            DIYProject(
                name=p.get("name", ""),
                difficulty=p.get("difficulty", "easy"),
                time_minutes=p.get("time_minutes", 30),
                materials=p.get("materials", []),
                instructions=p.get("instructions", ""),
                estimated_cost=p.get("estimated_cost", 0),
            )
            for p in raw_diy
        ]

    scent_recs = None
    raw_scents = data.get("scent_recommendations") or (theme.scent_recommendations if hasattr(theme, "scent_recommendations") else None)
    if raw_scents and isinstance(raw_scents, list):
        scent_recs = [
            ScentRecommendation(
                scent=s.get("scent", ""),
                method=s.get("method", ""),
                placement=s.get("placement", ""),
                intensity=s.get("intensity", "medium"),
            )
            for s in raw_scents
        ]

    transition_tips = None
    if hasattr(theme, "transition_tips") and theme.transition_tips:
        transition_tips = theme.transition_tips if isinstance(theme.transition_tips, list) else None

    return SeasonalThemeResponse(
        id=str(theme.id),
        theme_type=theme.theme_type,
        season=theme.season,
        holiday=theme.holiday,
        name=theme.name,
        description=theme.description,
        color_palette=theme.color_palette,
        textures=data.get("textures") or theme.textures,
        materials=data.get("materials") or theme.materials,
        lighting_mood=theme.lighting_mood,
        decor_items=decor_items,
        diy_projects=diy_projects,
        scent_recommendations=scent_recs,
        music_playlist_mood=theme.music_playlist_mood,
        generated_image_url=theme.generated_image_url,
        budget_tier=theme.budget_tier,
        estimated_cost=theme.estimated_cost,
        reusability_score=theme.reusability_score,
        transition_from=theme.transition_from,
        transition_tips=transition_tips,
        is_favorite=theme.is_favorite,
        created_at=theme.created_at,
    )
