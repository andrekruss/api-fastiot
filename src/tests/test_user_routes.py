import pytest
from httpx import ASGITransport, AsyncClient

from main import app

@pytest.mark.asyncio
async def test_create_user(test_db):
    username = "myuser"
    email = "myuser@mail.com"
    password = "pass123"
    create_user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/users/register", json=create_user_data)
    assert response.status_code == 201
    assert response.json()["username"] == username
    assert response.json()["email"] == email

@pytest.mark.asyncio
async def test_me(test_db, test_token):

    headers = {
        "Authorization": f"Bearer {test_token['access_token']}"
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/users/me", headers=headers)

    assert response.status_code == 200

