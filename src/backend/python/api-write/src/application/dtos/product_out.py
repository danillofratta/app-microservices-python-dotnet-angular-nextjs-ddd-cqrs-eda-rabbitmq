from pydantic import BaseModel
from decimal import Decimal

class ProductOut(BaseModel):
    product_id: str
    quantity: int
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: float  # Automatically convert Decimal to float for JSON
        }