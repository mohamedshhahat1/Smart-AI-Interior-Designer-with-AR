from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.request_models import (
    Room3DGenerateRequest,
    WalkthroughStartRequest,
    WalkthroughEndRequest,
)
from backend.app.schemas.response_models import (
    Room3DModelResponse,
    Room3DSummary,
    WalkthroughSessionResponse,
    Furniture3DObject,
    LightSource3D,
    CameraPosition,
    WalkthroughPathPoint,
)
from backend.app.services.walkthrough_3d_service import walkthrough_3d_service
from backend.app.services.storage_service import storage_service
from backend.app.core.security import get_current_user_id

router = APIRouter(prefix="/3d", tags=["3D Walkthrough / Room Generation"])


@router.post("/generate", response_model=Room3DModelResponse, status_code=status.HTTP_201_CREATED)
async def generate_3d_model(
    request: Room3DGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    model = await walkthrough_3d_service.generate_3d_model(
        db=db, user_id=user_id,
        room_type=request.room_type, name=request.name,
        room_id=request.room_id, design_id=request.design_id,
        quality_level=request.quality_level,
        reconstruction_method=request.reconstruction_method,
        room_dimensions=request.room_dimensions,
        detected_objects=request.detected_objects,
        include_furniture=request.include_furniture,
        include_lighting=request.include_lighting,
        generate_walkthrough_path=request.generate_walkthrough_path,
        output_formats=request.output_formats,
    )
    return _model_to_response(model)


@router.get("/models", response_model=list[Room3DSummary])
async def list_3d_models(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    models = await walkthrough_3d_service.get_user_models(db, user_id)
    return [
        Room3DSummary(
            id=str(m.id), name=m.name, room_type=m.room_type,
            status=m.status, quality_level=m.quality_level,
            glb_model_url=storage_service.to_public_url(m.glb_model_url),
            polygon_count=m.polygon_count,
            view_count=m.view_count, created_at=m.created_at,
        )
        for m in models
    ]


@router.get("/models/{model_id}", response_model=Room3DModelResponse)
async def get_3d_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    model = await walkthrough_3d_service.get_model(db, model_id)
    if not model or str(model.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="3D model not found")
    await walkthrough_3d_service.increment_view(db, model)
    return _model_to_response(model)


@router.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_3d_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    model = await walkthrough_3d_service.get_model(db, model_id)
    if not model or str(model.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="3D model not found")
    await walkthrough_3d_service.delete_model(db, model)


@router.post("/walkthrough/start", response_model=WalkthroughSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_walkthrough(
    request: WalkthroughStartRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    model = await walkthrough_3d_service.get_model(db, request.model_id)
    if not model or str(model.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="3D model not found")

    session = await walkthrough_3d_service.start_walkthrough(
        db, user_id, request.model_id, request.comparison_model_id,
    )
    return WalkthroughSessionResponse(
        id=str(session.id), model_id=str(session.model_id),
        comparison_model_id=str(session.comparison_model_id) if session.comparison_model_id else None,
        started_at=session.started_at,
    )


@router.post("/walkthrough/end", response_model=WalkthroughSessionResponse)
async def end_walkthrough(
    request: WalkthroughEndRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    session = await walkthrough_3d_service.end_walkthrough(
        db, request.session_id,
        camera_path=request.camera_path_taken,
        screenshots=request.screenshots_taken,
        annotations=request.annotations,
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    return WalkthroughSessionResponse(
        id=str(session.id), model_id=str(session.model_id),
        comparison_model_id=str(session.comparison_model_id) if session.comparison_model_id else None,
        duration_seconds=session.duration_seconds,
        screenshots_taken=session.screenshots_taken,
        started_at=session.started_at, ended_at=session.ended_at,
    )


def _model_to_response(model) -> Room3DModelResponse:
    furniture = None
    if model.furniture_3d_objects:
        furniture = [Furniture3DObject(**f) for f in model.furniture_3d_objects]

    lighting = None
    if model.lighting_setup:
        lighting = [LightSource3D(**l) for l in model.lighting_setup]

    cameras = None
    if model.camera_positions:
        cameras = [CameraPosition(**c) for c in model.camera_positions]

    walkthrough = None
    if model.walkthrough_path:
        walkthrough = [WalkthroughPathPoint(**p) for p in model.walkthrough_path]

    return Room3DModelResponse(
        id=str(model.id), name=model.name, room_type=model.room_type,
        status=model.status, reconstruction_method=model.reconstruction_method,
        quality_level=model.quality_level, dimensions=model.dimensions,
        room_geometry=model.room_geometry,
        depth_map_url=storage_service.to_public_url(model.depth_map_url),
        mesh_url=storage_service.to_public_url(model.mesh_url),
        glb_model_url=storage_service.to_public_url(model.glb_model_url),
        usdz_model_url=storage_service.to_public_url(model.usdz_model_url),
        furniture_objects=furniture,
        lighting_setup=lighting, camera_positions=cameras,
        walkthrough_path=walkthrough, polygon_count=model.polygon_count,
        file_size_mb=model.file_size_mb,
        processing_time_seconds=model.processing_time_seconds,
        view_count=model.view_count,
        room_id=str(model.room_id) if model.room_id else None,
        design_id=str(model.design_id) if model.design_id else None,
        created_at=model.created_at,
    )
