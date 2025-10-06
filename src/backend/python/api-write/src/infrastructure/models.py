import enum
from lib2to3.pytree import Base
from sqlalchemy import JSON, UUID, Column, Enum, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID 
import datetime, uuid

class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"


class OrderModel(Base):
    __tablename__ = "Orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String, nullable=False)
    items = Column(JSON, nullable=False)  # Store list of dicts directly in Postgres JSONB
    total = Column(Float, nullable=False)
    status = Column(
        Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]),
        default=OrderStatus.PENDING,
        nullable=False
    )
    created_at = Column(DateTime, nullable=False)
