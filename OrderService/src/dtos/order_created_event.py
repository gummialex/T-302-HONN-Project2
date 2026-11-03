from dataclasses import dataclass

@dataclass
class OrderCreatedEvent:
    orderId: int
    productId: int
    productName: str
    merchantId: int
    buyerId: int
    totalPrice: float
    creditCard: dict
    buyerEmail: str
    merchantEmail: str