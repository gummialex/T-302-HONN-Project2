from fastapi import APIRouter, HTTPException, Depends
from src.dtos.buyer_dto import Buyer
from src.infrastructure.get_service import get_buyer_service
from src.services.buyer_service import BuyerService


router = APIRouter(prefix='/buyers')
    
@router.post("", status_code=201)
def create_buyer(buyer: Buyer, buyer_service: BuyerService = Depends(get_buyer_service)):
    return buyer_service.create_buyer(buyer)


@router.get("/{buyer_id}", response_model=Buyer)
def get_buyer(buyer_id: int, buyer_service: BuyerService = Depends(get_buyer_service)):
    buyer = buyer_service.get_buyer(buyer_id)
    
    if buyer is None:
        raise HTTPException(
            status_code=404,
            detail="buyer does not exist"
        )
    return buyer
