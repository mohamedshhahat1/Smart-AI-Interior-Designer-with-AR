import pytest
from tests.conftest import auth_header


class TestRegister:
    @pytest.mark.asyncio
    async def test_register_success(self, async_client):
        resp = await async_client.post("/api/v1/auth/register", json={
            "name": "Alice", "email": "alice@test.com", "password": "secure1234",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "alice@test.com"
        assert data["expires_in"] > 0

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, async_client, test_user):
        user, _, _ = test_user
        resp = await async_client.post("/api/v1/auth/register", json={
            "name": "Bob", "email": user.email, "password": "secure1234",
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_register_weak_password(self, async_client):
        resp = await async_client.post("/api/v1/auth/register", json={
            "name": "Eve", "email": "eve@test.com", "password": "short",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, async_client):
        resp = await async_client.post("/api/v1/auth/register", json={
            "name": "Bad", "email": "not-an-email", "password": "secure1234",
        })
        assert resp.status_code == 422


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success(self, async_client, test_user):
        user, _, _ = test_user
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": user.email, "password": "testpassword123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, async_client, test_user):
        user, _, _ = test_user
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": user.email, "password": "wrongpassword",
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, async_client):
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "nobody@test.com", "password": "whatever123",
        })
        assert resp.status_code == 401


class TestRefreshToken:
    @pytest.mark.asyncio
    async def test_refresh_with_valid_token(self, async_client, test_user):
        _, _, refresh_token = test_user
        resp = await async_client.post(
            "/api/v1/auth/refresh",
            headers=auth_header(refresh_token),
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    @pytest.mark.asyncio
    async def test_refresh_with_access_token_fails(self, async_client, test_user):
        _, access_token, _ = test_user
        resp = await async_client.post(
            "/api/v1/auth/refresh",
            headers=auth_header(access_token),
        )
        assert resp.status_code == 401


class TestProtectedEndpoints:
    @pytest.mark.asyncio
    async def test_access_without_token(self, async_client):
        resp = await async_client.get("/api/v1/room/")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_access_with_valid_token(self, async_client, test_user):
        _, token, _ = test_user
        resp = await async_client.get(
            "/api/v1/room/",
            headers=auth_header(token),
        )
        assert resp.status_code == 200


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_health(self, async_client):
        resp = await async_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root(self, async_client):
        resp = await async_client.get("/")
        assert resp.status_code == 200
        assert "status" in resp.json()
