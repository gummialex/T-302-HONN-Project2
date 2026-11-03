import json
from dataclasses import asdict

import pika

from dtos.order_created_event import OrderCreatedEvent

class EventPublisher:

    def __init__(self, rabbitmq_url: str):
        self._parameters = pika.URLParameters(rabbitmq_url)

    def publish_order_created(self, event: OrderCreatedEvent) -> None:

        body = json.dumps(asdict(event))

        connection = pika.BlockingConnection(self._parameters)

        try:
            channel = connection.channel()

            channel.exchange_declare(
                exchange="order_events",
                exchange_type="topic",
                durable=True,
            )

            channel.basic_publish(
                exchange="order_events",
                routing_key="order.created",
                body=body,
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )
        finally:
            connection.close()