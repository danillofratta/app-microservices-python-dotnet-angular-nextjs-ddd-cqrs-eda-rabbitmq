from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import uuid4

@dataclass
class Order:
    id: str
    customer_id: str
    items: List[dict]
    total: float
    status: str
    created_at: datetime

    def __init__(self, customer_id: str, items: List[dict]):
        self.id = str(uuid4())
        self.customer_id = customer_id
        self.items = items or []
        self.total = sum(item["price"] * item["quantity"] for item in items)
        self.status = "Pending"
        self.created_at = datetime.utcnow()