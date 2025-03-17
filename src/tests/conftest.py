import logging
from bson import ObjectId
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from api_responses.auth_responses import TokenResponse
from api_responses.project_responses import ProjectResponse
from api_responses.user_responses import UserResponse
from app_secrets import TEST_DATABASE_NAME, TEST_DATABASE_URL
from database.models.user_model import User
from database.models.project_model import Project
from database.models.module_model import Module
from utils.hash import hash_password, verify_password
from utils.token import generate_jwt_token

logging.basicConfig(level=logging.DEBUG)

@pytest_asyncio.fixture(scope="function")
async def test_db():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    database = client[TEST_DATABASE_NAME]
    logging.debug("Initializing Beanie...")

    await init_beanie(
        database=database,
        document_models=[User, Project, Module]
    )

    try:
        yield database  
    finally:
        collections = await database.list_collection_names()  
        for collection in collections:
            await database[collection].delete_many({})  

        client.close()

@pytest_asyncio.fixture(scope="function")
async def test_user(test_db):
    username = "testuser"
    email = "testuser@mail.com"
    password = "testpass123"
    hashed_password = hash_password(password)

    existing_user = await User.find_one({"username": username})
    if not existing_user:
        user = User(
            username=username,
            email=email,
            password=hashed_password
        )
        await user.insert()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": password,
        "projects": user.projects
    }

@pytest_asyncio.fixture(scope="function")
async def test_token(test_db, test_user):

    user = await User.find_one(
        {"$or": [{"email": test_user["email"]}, {"username": test_user["username"]}]}
    )

    if user and verify_password(test_user["password"], user.password):
        jwt_token = generate_jwt_token({"sub": user.email})
        return {
            "access_token": jwt_token
        }
     
@pytest_asyncio.fixture(scope="function")
async def test_project(test_user):

    test_project_name = "project"
    test_project_description = "my project description"

    project = Project(
        user_id=ObjectId(test_user["id"]),
        name=test_project_name,
        description=test_project_description
    )

    await project.insert()

    return {
        "id": project.id,
        "user_id": project.user_id,
        "name": project.name,
        "description": project.description,
        "modules": project.modules
    }




        



    