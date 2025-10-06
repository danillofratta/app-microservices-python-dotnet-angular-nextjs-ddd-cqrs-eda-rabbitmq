from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Product:
    def __init__(self, id: str, quantity: int, price: Decimal):
        self.id = id
        self.quantity = quantity
        self.price = price