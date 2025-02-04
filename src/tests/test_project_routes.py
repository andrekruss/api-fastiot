import asyncio
import pytest
from httpx import ASGITransport, AsyncClient

from main import app

@pytest.mark.asyncio
async def test_create_project(test_token):

    test_project_name = "testproject"
    test_project_description = "my project description"

    headers = {
        "Authorization": f"Bearer {test_token['access_token']}"
    }

    create_project_json = {
        "name": test_project_name,
        "description": test_project_description
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/projects/create", headers=headers, json=create_project_json)

    assert response.status_code == 201
    assert response.json()["name"] == test_project_name
    assert response.json()["description"] == test_project_description

@pytest.mark.asyncio
async def test_get_project(test_token, test_project):

    access_token = test_token['access_token']
    project_id = str(test_project["id"])

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get(f"/projects/get/{project_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == test_project["name"]
    
@pytest.mark.asyncio
async def test_list_projects(test_token, test_project):

    access_token = test_token['access_token']

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/projects/list", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_project(test_token, test_project):

    access_token = test_token['access_token']
    project_id = str(test_project["id"])

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.delete(f"/projects/delete/{project_id}", headers=headers)

    assert response.status_code == 204

@pytest.mark.asyncio
async def test_patch_project(test_token, test_project):

    access_token = test_token['access_token']
    project_id = str(test_project["id"])
    updated_project_name = "new project name"
    updated_project_description = "new project description"

    patch_project_data = {
        "name": updated_project_name,
        "description": updated_project_description
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.patch(f"/projects/patch/{project_id}", headers=headers, json=patch_project_data)

    assert response.status_code == 200
    assert response.json()["name"] == updated_project_name
    assert response.json()["description"] == updated_project_description

    