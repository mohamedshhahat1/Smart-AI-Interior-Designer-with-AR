import os
import uuid
import time
import logging
from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.walkthrough_3d import Room3DModel, WalkthroughSession
from backend.app.models.room import Room

from ai_services.reconstruction_3d.depth_estimator import depth_estimator
from ai_services.reconstruction_3d.mesh_generator import mesh_generator
from ai_services.reconstruction_3d.scene_builder import scene_builder

logger = logging.getLogger(__name__)


class Walkthrough3DService:
    async def generate_3d_model(
        self,
        db: AsyncSession,
        user_id: str,
        room_type: str,
        name: str = "My 3D Room",
        room_id: Optional[str] = None,
        design_id: Optional[str] = None,
        quality_level: str = "standard",
        reconstruction_method: str = "depth_estimation",
        room_dimensions: Optional[dict] = None,
        detected_objects: Optional[list[dict]] = None,
        include_furniture: bool = True,
        include_lighting: bool = True,
        generate_walkthrough_path: bool = True,
        output_formats: list[str] = None,
    ) -> Room3DModel:
        start_time = time.time()

        model = Room3DModel(
            user_id=uuid.UUID(user_id),
            room_id=uuid.UUID(room_id) if room_id else None,
            design_id=uuid.UUID(design_id) if design_id else None,
            name=name,
            room_type=room_type,
            quality_level=quality_level,
            reconstruction_method=reconstruction_method,
            status="processing",
        )
        db.add(model)
        await db.flush()

        if room_id and (not detected_objects or not room_dimensions):
            result = await db.execute(select(Room).where(Room.id == uuid.UUID(room_id)))
            room = result.scalar_one_or_none()
            if room:
                if not detected_objects and room.detected_objects:
                    detected_objects = room.detected_objects if isinstance(room.detected_objects, list) else []
                if not room_dimensions and room.area:
                    side = room.area ** 0.5
                    room_dimensions = {"width": round(side * 1.2, 1), "depth": round(side / 1.2, 1), "height": 2.8}

        if not room_dimensions:
            room_dimensions = {"width": 5.0, "depth": 4.0, "height": 2.8}

        try:
            room_geometry = mesh_generator.generate_room_mesh(room_dimensions, quality_level)

            furniture_objects = []
            if include_furniture:
                furniture_objects = mesh_generator.place_furniture(detected_objects, room_dimensions)

            lighting_setup = []
            if include_lighting:
                lighting_setup = mesh_generator.generate_lighting(room_dimensions, furniture_objects)

            camera_positions = scene_builder.build_camera_positions(room_dimensions)

            walkthrough_path = []
            if generate_walkthrough_path:
                walkthrough_path = scene_builder.build_walkthrough_path(
                    room_dimensions, furniture_objects, path_type="tour"
                )

            scene = scene_builder.compose_scene(
                room_geometry=room_geometry,
                furniture_objects=furniture_objects,
                lighting=lighting_setup,
                camera_positions=camera_positions,
                walkthrough_path=walkthrough_path,
                quality_level=quality_level,
            )

            processing_time = time.time() - start_time

            model.room_geometry = room_geometry
            model.furniture_3d_objects = furniture_objects
            model.lighting_setup = lighting_setup
            model.camera_positions = camera_positions
            model.walkthrough_path = walkthrough_path
            model.dimensions = room_dimensions
            model.polygon_count = scene["metadata"]["polygon_count"]
            model.file_size_mb = scene["metadata"]["file_size_mb"]
            model.processing_time_seconds = round(processing_time, 2)

            glb_path = f"/tmp/3d_models/{model.id}.glb"
            exported = mesh_generator.export_to_glb(
                room_geometry, furniture_objects, lighting_setup, glb_path
            )

            if exported and os.path.exists(glb_path):
                model.file_size_mb = round(os.path.getsize(glb_path) / (1024 * 1024), 3)
                try:
                    from backend.app.services.storage_service import storage_service
                    object_name = f"3d_models/{model.id}.glb"
                    with open(glb_path, "rb") as f:
                        storage_service.upload_bytes(
                            object_name, f.read(), content_type="model/gltf-binary"
                        )
                    model.glb_model_url = storage_service.get_internal_url(object_name)
                except Exception as e:
                    logger.warning("MinIO upload failed, using local path: %s", e)
                    model.glb_model_url = glb_path
            else:
                model.glb_model_url = f"/storage/3d_models/{model.id}.glb"

            model.usdz_model_url = None
            model.status = "completed"

        except Exception as e:
            model.status = "failed"
            model.error_message = str(e)
            model.processing_time_seconds = round(time.time() - start_time, 2)

        await db.flush()
        return model

    async def get_model(self, db: AsyncSession, model_id: str) -> Optional[Room3DModel]:
        result = await db.execute(
            select(Room3DModel).where(Room3DModel.id == uuid.UUID(model_id))
        )
        return result.scalar_one_or_none()

    async def get_user_models(self, db: AsyncSession, user_id: str) -> list[Room3DModel]:
        result = await db.execute(
            select(Room3DModel)
            .where(Room3DModel.user_id == uuid.UUID(user_id))
            .order_by(Room3DModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def increment_view(self, db: AsyncSession, model: Room3DModel):
        model.view_count += 1
        await db.flush()

    async def start_walkthrough(
        self, db: AsyncSession, user_id: str,
        model_id: str, comparison_model_id: Optional[str] = None,
    ) -> WalkthroughSession:
        session = WalkthroughSession(
            user_id=uuid.UUID(user_id),
            model_id=uuid.UUID(model_id),
            comparison_model_id=uuid.UUID(comparison_model_id) if comparison_model_id else None,
        )
        db.add(session)
        await db.flush()
        return session

    async def end_walkthrough(
        self, db: AsyncSession, session_id: str,
        camera_path: Optional[list[dict]] = None,
        screenshots: int = 0,
        annotations: Optional[list[dict]] = None,
    ) -> Optional[WalkthroughSession]:
        result = await db.execute(
            select(WalkthroughSession).where(WalkthroughSession.id == uuid.UUID(session_id))
        )
        session = result.scalar_one_or_none()
        if not session:
            return None

        session.ended_at = datetime.now(timezone.utc)
        if session.started_at:
            session.duration_seconds = (session.ended_at - session.started_at).total_seconds()
        session.camera_path_taken = camera_path
        session.screenshots_taken = screenshots
        session.annotations = annotations
        await db.flush()
        return session

    async def delete_model(self, db: AsyncSession, model: Room3DModel):
        await db.delete(model)


walkthrough_3d_service = Walkthrough3DService()
