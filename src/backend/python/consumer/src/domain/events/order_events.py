from dataclasses import dataclass
from typing import List

@dataclass
class OrderCreatedEvent:
    order_id: str
    customer_id: str
    items: List[dict]
    total: float