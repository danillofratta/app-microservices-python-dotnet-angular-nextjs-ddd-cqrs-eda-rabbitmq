
from domain.repositories.mongo_order_repository_inteface import IMongoOrderRepository

class GetAllOrderQuery:
    def __init__(self, repo: IMongoOrderRepository):
        self.repo = repo

    async def execute(self) -> dict:
        order = await self.repo.get_all()
        if not order:
            raise ValueError(f"Orders not found")
        return order