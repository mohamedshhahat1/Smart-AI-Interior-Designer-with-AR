import io
import pytest
from unittest.mock import AsyncMock, patch
from backend.tests.conftest import auth_header


class TestRoomUpload:
    @pytest.mark.asyncio
    async def test_upload_requires_auth(self, async_client):
        fake_image = io.BytesIO(b"\xff\xd8\xff" + b"\x00" * 100)
        resp = await async_client.post(
            "/api/v1/room/upload",
            files={"file": ("room.jpg", fake_image, "image/jpeg")},
        )
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_upload_invalid_content_type(self, async_client, test_user):
        _, token, _ = test_user
        resp = await async_client.post(
            "/api/v1/room/upload",
            files={"file": ("data.txt", b"hello world", "text/plain")},
            headers=auth_header(token),
        )
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_upload_success(self, async_client, test_user):
        _, token, _ = test_user
        mock_analysis = {
            "room_type": "living_room",
            "area": 25.0,
            "detected_objects": [],
            "segmentation_data": {},
        }
        with (
            patch(
                "backend.app.api.routes.room.ai_service.analyze_room",
                new=AsyncMock(return_value=mock_analysis),
            ),
            patch("backend.app.api.routes.room.storage_service.upload_bytes"),
            patch(
                "backend.app.api.routes.room.storage_service.get_internal_url",
                return_value="http://storage.test/rooms/test.jpg",
            ),
        ):
            fake_image = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 1024)
            resp = await async_client.post(
                "/api/v1/room/upload",
                files={"file": ("room.jpg", fake_image, "image/jpeg")},
                headers=auth_header(token),
            )
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["room_type"] == "living_room"


class TestRoomGet:
    @pytest.mark.asyncio
    async def test_get_room_invalid_uuid(self, async_client, test_user):
        _, token, _ = test_user
        resp = await async_client.get(
            "/api/v1/room/not-a-uuid",
            headers=auth_header(token),
        )
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_get_room_not_found(self, async_client, test_user):
        _, token, _ = test_user
        resp = await async_client.get(
            "/api/v1/room/00000000-0000-0000-0000-000000000000",
            headers=auth_header(token),
        )
        assert resp.status_code == 404


class TestRoomList:
    @pytest.mark.asyncio
    async def test_list_rooms_empty(self, async_client, test_user):
        _, token, _ = test_user
        resp = await async_client.get(
            "/api/v1/room/",
            headers=auth_header(token),
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
