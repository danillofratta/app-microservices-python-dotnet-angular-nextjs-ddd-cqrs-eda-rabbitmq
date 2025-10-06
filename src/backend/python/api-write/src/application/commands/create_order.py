from typing import List
from application.dtos.order_item_dto import OrderItemDto
from application.dtos.order_out import OrderOut
from core.logger import logger
from domain.entities.order import Order
from domain.entities.product import Product
from domain.events.order_events import OrderCreatedEvent
from domain.postgres_order_repository_interface import IPostgresOrderRepository
from infrastructure.event_bus.rabbitmq_publiser import RabbitMQPublisher
from application.dtos.order_out import ProductOut

command_logger = logger.getChild("command")

class CreateOrderCommand:
    def __init__(self, repo: IPostgresOrderRepository, publisher: RabbitMQPublisher):
        self.repo = repo
        self.publisher = publisher
        command_logger.debug(f"Initialized CreateOrderCommand with repo: {type(self.repo).__name__}")

    async def execute(self, customer_id: str, items: List[OrderItemDto]) -> OrderOut:
        command_logger.debug(f"Executing create order: customer_id={customer_id}, items_count={len(items)}")

        # Convert DTO items to Product entities
        products = [Product(id=i.product_id, quantity=i.quantity, price=i.price) for i in items]
        command_logger.debug(f"Created {len(products)} Product objects")
        
        order = Order.create(customer_id, products)
        command_logger.info(f"Created order: order_id={order.id}, total={order.total}")

        # Save the order to the repository
        try:
            await self.repo.save(order)
            command_logger.info(f"Saved order to repository: order_id={order.id}")
        except Exception as e:
            command_logger.error(f"Failed to save order: order_id={order.id}, error={str(e)}", exc_info=True)
            raise

        # Publish the order created event
        event = OrderCreatedEvent(order.id, order.customer_id, order.items, order.total)
        await self.publisher.publish("order.created", event)
        command_logger.info(f"Event OrderCreatedEvent: create")

        # Convert Product entities to ProductOut for the response
        product_outs = [ProductOut(product_id=p.id, quantity=p.quantity, price=p.price) for p in order.items]

        # Return OrderOut model
        return OrderOut(
            order_id=str(order.id),
            customer_id=order.customer_id,
            items=product_outs,
            total=order.total
        )