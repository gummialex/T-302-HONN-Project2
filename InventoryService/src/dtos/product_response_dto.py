from pydantic import BaseModel

class ProductResponseDTO(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int
