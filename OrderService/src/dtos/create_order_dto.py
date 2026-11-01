from pydantic import BaseModel

class CreditCard(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int


class CreateOrder(BaseModel):
    productID: int
    merchantID: int
    buyerID: int
    creditCard: CreditCard
    discount: float | None=None