from pydantic import BaseModel

class CreditCardDTO(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: str


class ProcessPaymentDTO(BaseModel):
    orderId: int
    productId: int
    creditCard: CreditCardDTO