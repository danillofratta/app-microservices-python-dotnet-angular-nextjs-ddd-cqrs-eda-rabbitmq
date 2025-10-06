import os
from infrastructure.event_bus.rabbitmq_publiser import RabbitMQPublisher

publisher_instance: RabbitMQPublisher | None = None

async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    global publisher_instance
    if not publisher_instance:
        publisher_instance = RabbitMQPublisher(os.getenv("RABBITMQ_URL"))
        await publisher_instance.connect()  
    return publisher_instance
