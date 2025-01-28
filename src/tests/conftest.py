import logging
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app_secrets import TEST_DATABASE_NAME, TEST_DATABASE_URL
from database.models.user_model import User
from database.models.project_model import Project
from database.models.module_model import Module

logging.basicConfig(level=logging.DEBUG)

@pytest_asyncio.fixture(scope="function")
async def test_db():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    database = client[TEST_DATABASE_NAME]
    logging.debug("Inicializando Beanie com os modelos...")

    # Inicializa o Beanie com os modelos
    await init_beanie(
        database=database,
        document_models=[User, Project, Module]
    )
    logging.debug("Beanie inicializado com sucesso.")

    # Limpa o banco de dados após cada teste
    yield database

    # Função de limpeza
    collections = await database.list_collection_names()  # Aguarda a lista de coleções
    for collection in collections:
        collection_instance = database[collection]
        await collection_instance.delete_many({})  # Limpa os documentos

    client.close()  # Fecha a conexão com o banco de dados após o teste
