from fastapi import Depends
from domain.repositories.mongo_order_repository_inteface import IMongoOrderRepository
from infrastructure.repositories.mongo_order_repository import MongoOrderRepository
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def get_mongo_client():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    try:
        yield client
    finally:
        client.close()

async def get_order_repository(client: AsyncIOMotorClient = Depends(get_mongo_client)) -> IMongoOrderRepository:
    return MongoOrderRepository(client)