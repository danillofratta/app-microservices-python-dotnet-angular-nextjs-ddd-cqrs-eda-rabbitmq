from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient

from domain.repositories.mongo_order_repository_inteface import IMongoOrderRepository

class MongoOrderRepository(IMongoOrderRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client["ecommerce_db"]["orders"]

    async def get_by_id(self, order_id: str) -> Optional[dict]:
        doc = await self.collection.find_one({"id": order_id})
        if doc:
            doc["_id"] = str(doc["_id"]) 
        return doc
    
    async def get_all(self) -> List[dict]:
        docs = []
        cursor = self.collection.find({})  
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  
            docs.append(doc)
        return docs

    async def get_by_customer(self, customer_id: str) -> List[dict]:
        cursor = self.collection.find({"customer_id": customer_id})
        results = []
        async for order in cursor:
            order["_id"] = str(order["_id"])
            results.append(order)
        return results