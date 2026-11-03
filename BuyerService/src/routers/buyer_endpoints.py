from fastapi import APIRouter, HTTPException
from src.dtos.buyer_dto import Buyer
from src.services.buyer_service import BuyerService


router = APIRouter()
buyer_service = BuyerService()
    
@router.post("/buyers", status_code=201)
def create_buyer(buyer: Buyer):
    buyer_id = buyer_service.create_buyer(buyer)

    return {"id": buyer_id}

@router.get("/buyers/{buyer_id}", response_model=Buyer)
def get_buyer(buyer_id: int):
    buyer = buyer_service.get_buyer(buyer_id)
    
    if buyer is None:
        raise HTTPException(
            status_code=404,
            detail="buyer does not exist"
        )
    return buyer
