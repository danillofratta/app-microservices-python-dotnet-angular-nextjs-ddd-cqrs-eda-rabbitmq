from typing import List, Optional, Protocol

class IMongoOrderRepository(Protocol):
    async def get_by_id(self, order_id: str) -> Optional[dict]:
        raise NotImplementedError
    
    async def get_all(self) -> List[dict]:
        raise NotImplementedError

    async def get_by_customer(self, customer_id: str) -> List[dict]:
        raise NotImplementedError