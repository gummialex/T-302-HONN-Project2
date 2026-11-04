
import os
import json
import pika

from src.infrastructure.get_service import get_inventory_service
from src.dtos.payment_result_dto import PaymentResultDTO


class RabbitMQConsumer:

    def __init__(self):
        self.inventory_service = get_inventory_service()

    def start(self):

        connection = pika.BlockingConnection(
            pika.URLParameters(os.environ["RABBITMQ_URL"])
        )

        try:
            channel = connection.channel()

            channel.exchange_declare(
                exchange="order_events",
                exchange_type="topic",
                durable=True
            )

            channel.queue_declare(
                queue="inventory_service",
                durable=True
            )

            channel.queue_bind(
                exchange="order_events",
                queue="inventory_service",
                routing_key="payment.succeeded"
            )

            channel.queue_bind(
                exchange="order_events",
                queue="inventory_service",
                routing_key="payment.failed"
            )

            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):

                event = json.loads(body.decode())

                result = PaymentResultDTO(
                    orderId=event["orderId"],
                    productId=event["productId"],
                    successful=event["successful"]
                )

                self.inventory_service.handle_payment_result(result)

                ch.basic_ack(delivery_tag=method.delivery_tag)

                print(f"Inventory updated for order {result.orderId}")

            channel.basic_consume(
                queue="inventory_service",
                on_message_callback=callback,
                auto_ack=False
            )

            print("InventoryService listening for payments...")
            channel.start_consuming()

        finally:
            if connection.is_open:
                connection.close()
