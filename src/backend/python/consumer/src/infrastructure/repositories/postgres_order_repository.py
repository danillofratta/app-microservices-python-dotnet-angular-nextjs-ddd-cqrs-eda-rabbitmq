from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json

from domain.entities.order import Order
from domain.repositories.postgres_order_repository_interface import IPostgresOrderRepository

class PostgresOrderRepository(IPostgresOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, order: Order):
        query = """
        INSERT INTO orders (id, customer_id, items, total, status, created_at)
        VALUES (:id, :customer_id, :items, :total, :status, :created_at)
        """

        items_json = json.dumps(order.items) if order.items else "[]"

        await self.session.execute(text(query), {
            "id": order.id,
            "customer_id": order.customer_id,
            "items": items_json,
            "total": order.total,
            "status": order.status,
            "created_at": order.created_at
        })
        await self.session.commit()

    async def update(self, idorder: str, status: str):
        query = """
        UPDATE  orders SET status  = :status
        WHERE id =:id        
        """        
        await self.session.execute(text(query), {
            "id": idorder,            
            "status": status
        })
        await self.session.commit()          