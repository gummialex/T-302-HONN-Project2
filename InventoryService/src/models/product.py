from dataclasses import dataclass

@dataclass
class Product:
    merchantID: int
    pruductName: str
    price: float
    quantity: int
    reserved: int = 0
    id: int | None = None