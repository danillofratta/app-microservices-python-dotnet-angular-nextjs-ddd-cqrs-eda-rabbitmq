from dataclasses import dataclass
from datetime import datetime
import enum
from typing import List
from uuid import UUID, uuid4

from domain.entities.product import Product

class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"

@dataclass
class Order:
    id: UUID
    customer_id: str
    items: List[Product]
    total: float
    status: str
    created_at: datetime

    def __init__(self, customer_id: str, items: List[Product], _internal: bool = False):
        if not _internal:
            raise RuntimeError("Use Order.create() instead of calling Order() directly")

        self.id = str(uuid4())
        self.customer_id = customer_id
        self.items = items or []
        self.total = float(sum(item.price * item.quantity for item in items))
        self.status = "Pending"
        self.created_at = datetime.utcnow()

    @staticmethod
    def create(customer_id: str, items: List[Product]):
        return Order(customer_id, items, _internal=True)        