from dataclasses import dataclass


@dataclass
class Payment:
    orderId: int
    successful: bool