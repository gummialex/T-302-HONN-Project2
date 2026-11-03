
import os
import json
import pika

from src.services.email_service import EmailService


class RabbitMQConsumer:

    def __init__(self):
        self.email_service = EmailService()

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
                queue="email_service",
                durable=True
            )

            channel.queue_bind(
                exchange="order_events",
                queue="email_service",
                routing_key="order.created"
            )

            channel.queue_bind(
                exchange="order_events",
                queue="email_service",
                routing_key="payment.succeeded"
            )

            channel.queue_bind(
                exchange="order_events",
                queue="email_service",
                routing_key="payment.failed"
            )

           
            def callback(ch, method, properties, body):

                event = json.loads(body.decode())

                print(f"Received event: {method.routing_key}")

                if method.routing_key == "order.created":
                    self.email_service.order_created(event)

                elif method.routing_key == "payment.succeeded":
                    self.email_service.payment_succeeded(event)

                elif method.routing_key == "payment.failed":
                    self.email_service.payment_failed(event)

                else:
                    raise ValueError(
                        f"Unknown event: {method.routing_key}"
                    )

                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(f"Successfully processed: {method.routing_key}")

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue="email_service",
                on_message_callback=callback,
                auto_ack=False
            )

            print("EmailService listening for events...")
            channel.start_consuming()

        finally:
            if connection.is_open:
                connection.close()
