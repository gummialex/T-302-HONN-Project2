from pydantic import BaseModel, Field

class CreateProductDTO(BaseModel):
    merchantId: int
    pruductName: str
    price: float
    quantity: int
    reserved: int
