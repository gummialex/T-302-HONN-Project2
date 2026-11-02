from fastapi import APIRouter, HTTPException
from src.dtos.merchant_dto import Merchant
from src.services.merchant_service import MerchantService


router = APIRouter()
merchant_service = MerchantService()
    
@router.post("/merchants", status_code=201)
def create_merchant(merchant: Merchant):
    merchant_id = merchant_service.create_merchant(merchant)

    return {"id": merchant_id}

@router.get("/merchants/{merchant_id}", response_model=Merchant)
def get_merchant(merchant_id: int):
    merchant = merchant_service.get_merchant(merchant_id)
    
    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant does not exist"
        )
    return merchant
