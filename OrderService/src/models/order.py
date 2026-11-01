from dataclasses import dataclass


@dataclass
class Order:
    id: int = None
    productId: int
    merchantId: int
    buyerId: int
    cardNumber: str
    totalPrice: float