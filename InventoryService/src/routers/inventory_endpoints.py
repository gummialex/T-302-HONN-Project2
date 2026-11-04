from fastapi import APIRouter, HTTPException

from src.dtos.create_product_dto import CreateProductDTO
from src.dtos.product_response_dto import ProductResponseDTO
from src.dtos.reserve_product_dto import ReserveProductDTO

from src.dependencies import inventory_service as service


router = APIRouter()


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

@router.post("/products/{product_id}/reserve")
def reserve_product(
    product_id: int,
    request: ReserveProductDTO,
):
    try:
        service.reserve_product(product_id, request.orderId)
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error

    return {"message": "Product reserved"}