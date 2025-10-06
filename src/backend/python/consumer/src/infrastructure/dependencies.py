import os
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from domain.repositories.mongo_order_repository_interface import IMongoOrderRepository
from domain.repositories.postgres_order_repository_interface import IPostgresOrderRepository
from infrastructure.repositories.mongo_order_repository import MongoOrderRepository
from infrastructure.repositories.postgres_order_repository import PostgresOrderRepository
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URL")
MONGO_URL = os.getenv("MONGO_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_postgres_repo() -> AsyncGenerator[IPostgresOrderRepository, None]:
    async with AsyncSessionLocal() as session:
        yield PostgresOrderRepository(session)

# Mongo
async def get_mongo_repo() -> IMongoOrderRepository:
    client = AsyncIOMotorClient(MONGO_URL)
    return MongoOrderRepository(client)