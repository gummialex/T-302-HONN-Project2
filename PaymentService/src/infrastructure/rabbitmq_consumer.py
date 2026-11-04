
import os
import json
import pika

from src.dependencies import payment_service
from src.dtos.process_payment_dto import ProcessPaymentDTO


class RabbitMQConsumer:

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
                queue="payment_service",
                durable=True
            )

            channel.queue_bind(
                exchange="order_events",
                queue="payment_service",
                routing_key="order.created"
            )

            channel.confirm_delivery()
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):

                event = json.loads(body.decode())

                request = ProcessPaymentDTO(
                    orderId=event["orderId"],
                    productId=event["productId"],
                    creditCard=event["creditCard"]
                )

                payment = payment_service.process_payment(request)

                if payment.successful:
                    routing_key = "payment.succeeded"
                else:
                    routing_key = "payment.failed"

                result = {
                    "orderId": payment.orderId,
                    "productId": payment.productId,
                    "successful": payment.successful,
                    "buyerEmail": event["buyerEmail"],
                    "merchantEmail": event["merchantEmail"]
                }

                ch.basic_publish(
                    exchange="order_events",
                    routing_key=routing_key,
                    body=json.dumps(result),
                    mandatory=True,
                    properties=pika.BasicProperties(
                        content_type="application/json",
                        delivery_mode=pika.DeliveryMode.Persistent
                    )
                )

                ch.basic_ack(delivery_tag=method.delivery_tag)

                print(f"Processed order {payment.orderId}: {routing_key}")

            channel.basic_consume(
                queue="payment_service",
                on_message_callback=callback,
                auto_ack=False
            )

            print("PaymentService listening for orders...")
            channel.start_consuming()

        finally:
            if connection.is_open:
                connection.close()
