import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.request_models import (
    MoodDetectRequest,
    LightingSceneCreateRequest,
    LightingSceneUpdateRequest,
    CircadianScheduleRequest,
    MoodProfileCreateRequest,
    LightingFeedbackRequest,
    SmartHomeExportRequest,
)
from backend.app.schemas.response_models import (
    MoodDetectResponse,
    LightingSceneResponse,
    CircadianScheduleResponse,
    MoodProfileResponse,
    SmartHomeExportResponse,
    LightingInsightsResponse,
)
from backend.app.services.lighting_service import lighting_service
from backend.app.core.security import get_current_user_id

from ai_services.lighting.mood_analyzer import mood_analyzer
from ai_services.lighting.scene_generator import scene_generator
from ai_services.lighting.circadian_engine import circadian_engine
from ai_services.lighting.smart_home_export import smart_home_exporter

router = APIRouter(prefix="/lighting", tags=["Smart Lighting & Mood Detection"])


@router.post("/detect-mood", response_model=MoodDetectResponse)
async def detect_mood_and_recommend(
    request: MoodDetectRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    analysis = mood_analyzer.analyze(
        text_input=request.text_input,
        time_of_day=request.time_of_day,
        activity=request.activity,
        energy_level=request.energy_level,
    )

    recommendation = scene_generator.generate_scene(
        mood=analysis["detected_mood"],
        time_of_day=request.time_of_day,
        room_type=request.room_type,
        energy_level=analysis["energy_level"],
        warmth_score=analysis["warmth_score"],
    )

    alternatives = scene_generator.generate_alternatives(
        primary_mood=analysis["detected_mood"],
        suggested_moods=analysis["suggested_moods"],
        time_of_day=request.time_of_day,
        room_type=request.room_type,
    )

    circadian_note = None
    if request.time_of_day == "night" and analysis["detected_mood"] != "sleepy":
        circadian_note = (
            "It's nighttime — consider a warmer, dimmer setting to support "
            "melatonin production and better sleep quality."
        )
    elif request.time_of_day == "morning" and analysis["energy_level"] < 0.3:
        circadian_note = (
            "Morning detected with low energy — a bright, cool-white scene "
            "can help activate your circadian wake response."
        )

    return MoodDetectResponse(
        mood_analysis=analysis,
        lighting_recommendation=recommendation,
        alternative_scenes=alternatives,
        circadian_note=circadian_note,
    )


@router.post("/scenes", response_model=LightingSceneResponse, status_code=status.HTTP_201_CREATED)
async def create_scene(
    request: LightingSceneCreateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scene_data = {
        "color_temperature": request.color_temperature,
        "brightness": request.brightness,
        "color_hex": request.color_hex,
        "saturation": request.saturation,
        "fixtures": request.fixtures,
        "zones": request.zones,
        "transition_duration": request.transition_duration,
    }

    scene = await lighting_service.save_scene(
        db=db,
        user_id=user_id,
        scene_data=scene_data,
        name=request.name,
        mood=request.mood,
        room_id=request.room_id,
        design_id=request.design_id,
        time_of_day=request.time_of_day,
        activity=request.activity,
    )

    return _scene_to_response(scene)


@router.get("/scenes", response_model=list[LightingSceneResponse])
async def list_scenes(
    mood: str = None,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scenes = await lighting_service.get_user_scenes(db, user_id, mood)
    return [_scene_to_response(s) for s in scenes]


@router.get("/scenes/{scene_id}", response_model=LightingSceneResponse)
async def get_scene(
    scene_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scene = await lighting_service.get_scene(db, scene_id)
    if not scene or str(scene.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scene not found")
    return _scene_to_response(scene)


@router.patch("/scenes/{scene_id}", response_model=LightingSceneResponse)
async def update_scene(
    scene_id: str,
    request: LightingSceneUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scene = await lighting_service.get_scene(db, scene_id)
    if not scene or str(scene.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scene not found")

    if request.name is not None:
        scene.name = request.name
    if request.color_temperature is not None:
        scene.color_temperature = request.color_temperature
    if request.brightness is not None:
        scene.brightness = request.brightness
    if request.color_hex is not None:
        scene.color_hex = request.color_hex
    if request.saturation is not None:
        scene.saturation = request.saturation
    if request.transition_duration is not None:
        scene.transition_duration = request.transition_duration
    if request.is_favorite is not None:
        scene.is_favorite = request.is_favorite

    await db.flush()
    return _scene_to_response(scene)


@router.delete("/scenes/{scene_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scene(
    scene_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scene = await lighting_service.get_scene(db, scene_id)
    if not scene or str(scene.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scene not found")
    await db.delete(scene)


@router.post("/circadian", response_model=CircadianScheduleResponse)
async def generate_circadian_schedule(
    request: CircadianScheduleRequest,
    user_id: str = Depends(get_current_user_id),
):
    result = circadian_engine.generate_schedule(
        wake_time=request.wake_time,
        sleep_time=request.sleep_time,
        work_hours=request.work_hours,
        preferences=request.preferences,
    )
    return CircadianScheduleResponse(**result)


@router.post("/profiles", response_model=MoodProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_mood_profile(
    request: MoodProfileCreateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    profile = await lighting_service.save_mood_profile(db, user_id, request.model_dump())
    return MoodProfileResponse(
        id=str(profile.id),
        name=profile.name,
        mood_type=profile.mood_type,
        energy_level=profile.energy_level,
        warmth_preference=profile.warmth_preference,
        brightness_preference=profile.brightness_preference,
        preferred_colors=profile.preferred_colors,
        preferred_activities=profile.preferred_activities,
        is_active=profile.is_active,
        created_at=profile.created_at,
    )


@router.get("/profiles", response_model=list[MoodProfileResponse])
async def list_mood_profiles(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    profiles = await lighting_service.get_mood_profiles(db, user_id)
    return [
        MoodProfileResponse(
            id=str(p.id), name=p.name, mood_type=p.mood_type,
            energy_level=p.energy_level, warmth_preference=p.warmth_preference,
            brightness_preference=p.brightness_preference,
            preferred_colors=p.preferred_colors,
            preferred_activities=p.preferred_activities,
            is_active=p.is_active, created_at=p.created_at,
        )
        for p in profiles
    ]


@router.post("/feedback")
async def submit_feedback(
    request: LightingFeedbackRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    await lighting_service.record_feedback(
        db=db, user_id=user_id, scene_id=request.scene_id,
        mood=request.mood, rating=request.rating,
        duration_minutes=request.duration_minutes,
    )
    return {"status": "recorded"}


@router.post("/export", response_model=SmartHomeExportResponse)
async def export_to_smart_home(
    request: SmartHomeExportRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    scene = await lighting_service.get_scene(db, request.scene_id)
    if not scene or str(scene.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scene not found")

    scene_data = {
        "mood": scene.mood,
        "color_temperature": scene.color_temperature,
        "brightness": scene.brightness,
        "color_hex": scene.color_hex,
        "saturation": scene.saturation,
        "fixtures": scene.fixtures or [],
        "transition_duration": scene.transition_duration,
    }

    result = smart_home_exporter.export(scene_data, request.platform)
    return SmartHomeExportResponse(**result)


@router.get("/insights", response_model=LightingInsightsResponse)
async def get_lighting_insights(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    insights = await lighting_service.get_insights(db, user_id)
    return LightingInsightsResponse(**insights)


def _scene_to_response(scene: LightingScene) -> LightingSceneResponse:
    return LightingSceneResponse(
        id=str(scene.id),
        name=scene.name,
        mood=scene.mood,
        time_of_day=scene.time_of_day,
        activity=scene.activity,
        color_temperature=scene.color_temperature,
        brightness=scene.brightness,
        color_hex=scene.color_hex,
        saturation=scene.saturation,
        fixtures=scene.fixtures,
        zones=scene.zones,
        transition_duration=scene.transition_duration,
        is_circadian=scene.is_circadian,
        is_favorite=scene.is_favorite,
        usage_count=scene.usage_count,
        room_id=str(scene.room_id) if scene.room_id else None,
        design_id=str(scene.design_id) if scene.design_id else None,
        created_at=scene.created_at,
    )
