from pydantic import BaseModel, Field


class PaymentResultDTO(BaseModel):
    orderId: int = Field(gt=0)
    productId: int = Field(gt=0)
    successful: bool