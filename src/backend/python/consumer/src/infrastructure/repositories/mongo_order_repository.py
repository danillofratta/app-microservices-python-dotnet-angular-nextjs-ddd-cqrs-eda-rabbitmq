from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

from domain.repositories.mongo_order_repository_interface import IMongoOrderRepository

class MongoOrderRepository(IMongoOrderRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client["ecommerce_db"]["orders"]

    async def save(self, order: dict):        
        order.pop("_id", None)

        await self.collection.update_one(
            {"id": order["id"]},  
            {"$set": order},      
            upsert=True
        )

    async def get_by_id(self, order_id: str) -> Optional[dict]:
        doc = await self.collection.find_one({"id": order_id})
        if doc:
            doc["_id"] = str(doc["_id"]) 
        return doc