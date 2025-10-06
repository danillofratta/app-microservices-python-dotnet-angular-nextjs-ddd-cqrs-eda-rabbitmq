import asyncio
import aio_pika
import json
import logging
import os
from dotenv import load_dotenv
from infrastructure.dependencies import get_mongo_repo, get_postgres_repo

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_consumer():
    mongo_repo  = await  get_mongo_repo()
    post_repo = await anext(get_postgres_repo())

    # Conexão async com RabbitMQ
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    channel = await connection.channel()
   
    # Exchange
    exchange = await channel.declare_exchange("ecommerce_exchange", aio_pika.ExchangeType.TOPIC, durable=True)

    # Queue
    queue = await channel.declare_queue("order_queue", durable=True)
    await queue.bind(exchange, routing_key="order.created")
    await queue.bind(exchange, routing_key="stock.reserved")

    async def callback(message: aio_pika.IncomingMessage):
        async with message.process():
            event = json.loads(message.body)
            logger.info(f"Received event: {event}")

            if message.routing_key == "order.created":
                logger.info(f"Received order.created: {event}")
                order = {
                    "id": event["order_id"],
                    "customer_id": event["customer_id"],
                    "items": event["items"],
                    "total": event["total"],
                    "status": "Pending",
                    "created_at": event.get("created_at", None)
                }
                await mongo_repo.save(order)
                logger.info(f"Order saved: {order['id']}")
            elif message.routing_key == "stock.reserved":
                logger.info(f"Received tock.reserved: {event}")
                order = await mongo_repo.get_by_id(event["order_id"])
                if order:
                    order["status"] = "Confirmed" if event["success"] else "Failed"
                    await mongo_repo.save(order)
                    print(order)
                    logger.info(f"Order updated MONGO: {order['id']}")

                    await post_repo.update(order['id'], order['status'])                        
                    logger.info(f"Order updated POSTGRES: {order['id']}")
                     

    await queue.consume(callback)
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
     
    await asyncio.Future()  # loop 

# Entry point
if __name__ == "__main__":
    asyncio.run(start_consumer())
