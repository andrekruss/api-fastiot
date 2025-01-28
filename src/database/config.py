from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app_secrets import DATABASE_NAME, DATABASE_URL
from database.models.module_model import Module
from database.models.user_model import User
from database.models.project_model import Project

async def connect_to_db(connection_string: str = DATABASE_URL, db_name: str = DATABASE_NAME):

    client = AsyncIOMotorClient(connection_string)
    database = client[db_name]
    await init_beanie(
        database=database,
        document_models=[User, Project, Module]
    )