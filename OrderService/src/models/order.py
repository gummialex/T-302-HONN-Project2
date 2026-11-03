from dataclasses import dataclass


@dataclass
class Order:
    productId: int
    merchantId: int
    buyerId: int
    cardNumber: str
    totalPrice: float
    id: int = None