from pydantic import BaseModel, Field

class CreateProductDTO(BaseModel):
    merchantId: int
    pruductName: str = Field(min_length = 1)
    price: int = Field(ge = 0)
    quantity: int = Field(ge = 0)
