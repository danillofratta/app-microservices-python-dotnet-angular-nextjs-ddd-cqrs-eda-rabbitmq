import datetime
import select
from typing import List, Optional
from sqlalchemy.sql import text
import json
from domain.entities.order import Order
from domain.postgres_order_repository_interface import IPostgresOrderRepository
from infrastructure.database import AsyncSessionLocal
from infrastructure.models import OrderModel
from sqlalchemy.ext.asyncio import AsyncSession

class PostgresOrderRepository(IPostgresOrderRepository) :
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, order: Order):
        query = """
        INSERT INTO orders (id, customer_id, items, total, status, created_at)
        VALUES (:id, :customer_id, :items, :total, :status, :created_at)
        """
        
        items_json = json.dumps([
            {"product_id": item.id, "quantity": item.quantity, "price": float(item.price)}
            for item in order.items
        ]) if order.items else "[]"

        await self.session.execute(text(query), {
            "id": order.id,
            "customer_id": order.customer_id,
            "items": items_json,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at
        })
        await self.session.commit()

    async def get_all(self) -> List[Order]:
        query = text("SELECT id, customer_id, total, status FROM orders")
        result = await self.session.execute(query)
        rows = result.fetchall()

        orders: List[Order] = []

        for row in rows:
            data = dict(row._mapping)
            order = Order.__new__(Order)
            order.id = str(data["id"])
            order.customer_id = str(data["customer_id"])
            
            items_raw = data.get("items")
            if isinstance(items_raw, str) and items_raw.strip():
                order.items = json.loads(items_raw)
            elif isinstance(items_raw, list):
                order.items = items_raw
            else:
                order.items = []

            order.total = float(data["total"])
            order.status = str(data["status"])
            order.created_at = (
                data["created_at"] if isinstance(data["created_at"], datetime)
                else datetime.fromisoformat(str(data["created_at"]))
            )
            orders.append(order)

        return orders
    

class SqlOrderRepository(IPostgresOrderRepository):
    def __init__(self, session_factory=AsyncSessionLocal):
        self._session_factory = session_factory

    async def save(self, order: Order) -> None:
        async with self._session_factory() as session:
            items_json = [
                {"product_id": item.id, "quantity": item.quantity, "price": float(item.price)}
                for item in order.items
            ]
            model = OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                items=items_json,  # Store list of dictionaries
                total=float(order.total),
                status=order.status,
                created_at=order.created_at,
            )
            session.add(model)
            await session.commit()

    async def get_by_customer_id(self, customer_id: str) -> Optional[Order]:
        async with self._session_factory() as session:
            result = await session.execute(select(OrderModel).where(OrderModel.customer_id == customer_id))
            m = result.scalar_one_or_none()
            if not m:
                return None
            return Order(customer_id=m.customer_id, items=m.items)

    async def get_all(self) -> List[Order]:
        async with self._session_factory() as session:
            result = await session.execute(select(OrderModel))
            models = result.scalars().all()
            return [Order(customer_id=m.customer_id, items=m.items) for m in models]        