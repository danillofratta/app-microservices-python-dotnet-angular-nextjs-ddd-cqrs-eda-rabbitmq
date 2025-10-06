

from domain.repositories.mongo_order_repository_inteface import IMongoOrderRepository

class GetOrderQuery:
    def __init__(self, repo: IMongoOrderRepository):
        self.repo = repo

    async def execute(self, order_id: str) -> dict:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        return order