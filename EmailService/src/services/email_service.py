
from src.infrastructure.resend_client import ResendClient


class EmailService:

    def __init__(self):
        self.resend_client = ResendClient()

    def order_created(self, event: dict):

        recipients = [
            event["buyerEmail"],
            event["merchantEmail"]
        ]

        subject = "Order has been created"

        body = (
            f"Order {event['orderId']} has been created.\n"
            f"Product: {event['productName']}\n"
            f"Total price: {event['totalPrice']}"
        )

        self.resend_client.send_email(recipients, subject, body)

    def payment_succeeded(self, event: dict):

        recipients = [
            event["buyerEmail"],
            event["merchantEmail"]
        ]

        subject = "Order has been purchased"

        body = f"Order {event['orderId']} has been successfully purchased"

        self.resend_client.send_email(recipients, subject, body)

    def payment_failed(self, event: dict):

        recipients = [
            event["buyerEmail"],
            event["merchantEmail"]
        ]

        subject = "Order purchase failed"

        body = f"Order {event['orderId']} purchase has failed"

        self.resend_client.send_email(recipients, subject, body)
