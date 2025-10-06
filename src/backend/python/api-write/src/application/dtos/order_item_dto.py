from decimal import Decimal
from pydantic import BaseModel, Field, condecimal

class OrderItemDto(BaseModel):
    product_id: str
    quantity: int
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: float  # converte Decimal para float automaticamente
        }