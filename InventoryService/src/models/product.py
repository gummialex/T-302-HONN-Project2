from dataclasses import dataclass

@dataclass
class Product:
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0
    id: int | None = None