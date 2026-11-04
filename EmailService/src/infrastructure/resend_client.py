
import os
import resend


class ResendClient:

    def __init__(self):
        resend.api_key = os.environ["RESEND_API_KEY"]
        self.sender = os.environ["RESEND_FROM_EMAIL"]

    def send_email(self, recipients: list[str], subject: str, body: str):

        response = resend.Emails.send({
            "from": self.sender,
            "to": recipients,
            "subject": subject,
            "text": body
        })

        return response
