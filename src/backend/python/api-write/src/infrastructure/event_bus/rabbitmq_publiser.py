import aio_pika
import json
from dataclasses import asdict

class RabbitMQPublisher:
    def __init__(self, url: str):
        self.url = url
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None

    async def connect(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.declare_exchange(
                "ecommerce_exchange",
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )

    async def publish(self, routing_key: str, event):
        if not self.channel:
            raise Exception("Publisher not connected")
        exchange = await self.channel.get_exchange("ecommerce_exchange")
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(asdict(event)).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )
        print(f"[x] Sent event to {routing_key}: {event}")

    async def close(self):
        if self.connection:
            await self.connection.close()