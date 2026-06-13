from unittest.mock import MagicMock, patch

import pytest

from backend.app.models.design import Design
from backend.app.models.room import Room
from backend.app.services.storage_service import storage_service
from backend.tests.conftest import auth_header


class TestMediaProxy:
    @pytest.mark.asyncio
    async def test_rejects_parent_path(self, async_client):
        response = await async_client.get("/api/v1/media/../secret")
        assert response.status_code in (400, 404)

    @pytest.mark.asyncio
    async def test_streams_minio_object(self, async_client):
        minio_response = MagicMock()
        minio_response.headers = {"Content-Type": "image/jpeg"}
        minio_response.stream.return_value = [b"image-bytes"]
        minio_client = MagicMock()
        minio_client.get_object.return_value = minio_response

        with patch.object(storage_service, "_client", minio_client):
            response = await async_client.get("/api/v1/media/designs/result.jpg")

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
        assert response.content == b"image-bytes"
        minio_client.get_object.assert_called_once_with(
            "smart-interior", "designs/result.jpg"
        )
        minio_response.close.assert_called_once()
        minio_response.release_conn.assert_called_once()


class TestDesignMediaUrl:
    @pytest.mark.asyncio
    async def test_existing_minio_url_uses_backend_proxy(
        self, async_client, db, test_user
    ):
        user, token, _ = test_user
        room = Room(
            user_id=user.id,
            image_url="http://minio:9000/smart-interior/rooms/source.jpg",
            room_type="living_room",
        )
        db.add(room)
        await db.flush()

        design = Design(
            room_id=room.id,
            style="modern",
            generated_image_url=(
                "http://localhost:9000/smart-interior/designs/result.jpg"
            ),
        )
        db.add(design)
        await db.flush()

        response = await async_client.get(
            f"/api/v1/design/{design.id}",
            headers=auth_header(token),
        )

        assert response.status_code == 200
        assert response.json()["generated_image_url"] == (
            "http://test/api/v1/media/designs/result.jpg"
        )
