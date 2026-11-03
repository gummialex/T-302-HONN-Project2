from fastapi import APIRouter, HTTPException

from src.dtos.create_product_dto import CreateProductDTO
from src.dtos.product_response_dto import ProductResponseDTO
from src.infrastructure.repository import ProductRepository
from src.services.inventory_service import InventoryService


router = APIRouter()

repository = ProductRepository()
service = InventoryService(repository)


@router.post("/products", status_code=201)
def create_product(dto: CreateProductDTO):
    product_id = service.create_product(dto)
    return product_id

@router.get(
    "/products/{product_id}",
    response_model=ProductResponseDTO,
)
def get_product(product_id: int):
    product = service.get_product(product_id)

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

@router.post("/products/{product_id}/reserve", status_code=200)
def reserve_product(product_id: int):
    service.reserve_product(product_id)

    return {"message": "Product reserved"}