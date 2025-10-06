from decimal import Decimal
from typing import List
from pydantic import BaseModel
from application.dtos.product_out import ProductOut

class OrderOut(BaseModel):
    order_id: str
    customer_id: str
    items: List[ProductOut]
    total: Decimal

    class Config:
        json_encoders = {
            Decimal: float  # Automatically convert Decimal to float for JSON
        }