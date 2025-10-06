from typing import List
from pydantic import BaseModel

from application.dtos.order_item_dto import OrderItemDto

class CreateOrderDto(BaseModel):
    customer_id: str
    items: List[OrderItemDto]