from pydantic import BaseModel

class CreditCardDTO(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int


class ProcessPaymentDTO(BaseModel):
    orderId: int
    productId: int
    creditCard: CreditCardDTO