import pytest
from httpx import ASGITransport, AsyncClient

from main import app

@pytest.mark.asyncio
async def test_generate_token_with_username(test_user):
    
    login_request = {
        "username": test_user["username"],
        "password": test_user["password"]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/token", data=login_request)

    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_generate_token_with_email(test_user):
    
    login_request = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/token", data=login_request)

    assert response.status_code == 200
    assert "access_token" in response.json()