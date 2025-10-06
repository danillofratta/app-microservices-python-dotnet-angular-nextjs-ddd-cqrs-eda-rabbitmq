from dataclasses import dataclass
from typing import List

from domain.entities.product import Product

@dataclass
class OrderCreatedEvent:
    order_id: str
    customer_id: str
    items: List[Product]
    total: float

    def __init__(self, order_id: str, customer_id: str, items: List[Product], total: float):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total = float(total)