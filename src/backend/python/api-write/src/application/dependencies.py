from fastapi import Depends
from application.commands.create_order import CreateOrderCommand
from infrastructure.dependencies import get_order_repository
from infrastructure.event_bus.dependencies import get_rabbitmq_publisher

async def get_create_order_command(
    repo = Depends(get_order_repository),
    publisher = Depends(get_rabbitmq_publisher)
):
    return CreateOrderCommand(repo, publisher)
