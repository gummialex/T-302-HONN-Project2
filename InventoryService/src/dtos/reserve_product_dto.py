from pydantic import BaseModel, Field


class ReserveProductDTO(BaseModel):
    orderId: int = Field(gt=0)