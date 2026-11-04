from fastapi import APIRouter, HTTPException, Depends

from src.dtos.create_product_dto import CreateProductDTO
from src.dtos.product_response_dto import ProductResponseDTO
from src.infrastructure.get_service import get_inventory_service
from src.dtos.reserve_product_dto import ReserveProductDTO

from src.dependencies import inventory_service as service


router = APIRouter(prefix='/products')



@router.post("", status_code=201)
def create_product(dto: CreateProductDTO, inv_service: InventoryService = Depends(get_inventory_service)):
    return inv_service.create_product(dto)

@router.get("/{product_id}",response_model=ProductResponseDTO)
def get_product(product_id: int, inv_service: InventoryService = Depends(get_inventory_service)):
    product = inv_service.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product does not exist",
        )

    return ProductResponseDTO(
        merchantId=product.merchantId,
        productName=product.productName,
        price=product.price,
        quantity=product.quantity,
        reserved=product.reserved,
    )

@router.post("/{product_id}/reserve", status_code=200)
def reserve_product(product_id: int, inv_service: InventoryService = Depends(get_inventory_service)):
    inv_service.reserve_product(product_id)

    return {"message": "Product reserved"}