from fastapi import APIRouter, HTTPException, Depends
from src.dtos.merchant_dto import Merchant
from src.services.merchant_service import MerchantService
from src.infrastructure.get_service import get_merchant_service


router = APIRouter(prefix='/merchants')
    
@router.post("", status_code=201)
def create_merchant(merchant: Merchant, merchant_service: MerchantService = Depends(get_merchant_service)):
    return merchant_service.create_merchant(merchant)

@router.get("/{merchant_id}")
def get_merchant(merchant_id: int, merchant_service: MerchantService = Depends(get_merchant_service)):
    merchant = merchant_service.get_merchant(merchant_id)
    
    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant does not exist"
        )
    return merchant
