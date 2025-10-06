from abc import ABC, abstractmethod
from typing import List
from domain.entities.order import Order

class IPostgresOrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order): 
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self) -> List[Order]: 
        raise NotImplementedError