import logging
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

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
    logging.debug("Inicializando Beanie com os modelos...")

    await init_beanie(
        database=database,
        document_models=[User, Project, Module]
    )

    collections = await database.list_collection_names()  # Aguarda a lista de coleções
    for collection in collections:
        collection_instance = database[collection]
        await collection_instance.delete_many({})  # Limpa os documentos

    yield database

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
        "username": username,
        "email": email,
        "password": password
    }

@pytest_asyncio.fixture(scope="function")
async def test_token(test_db, test_user):

    user = await User.find_one(
        {"$or": [{"email": test_user["email"]}, {"username": test_user["username"]}]}
    )

    if user and verify_password(test_user["password"], user.password):
        jwt_token = generate_jwt_token({"sub": user.email})
        return {"access_token": jwt_token}


        



    