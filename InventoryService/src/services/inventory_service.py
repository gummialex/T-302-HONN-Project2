from src.dtos.create_product_dto import CreateProductDTO
from src.models.product import Product
from src.infrastructure.repository import ProductRepository
from fastapi import HTTPException


class InventoryService:

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def create_product(self, request: CreateProductDTO) -> int:
        product = Product(
            merchantId=request.merchantId,
            productName=request.productName,
            price=request.price,
            quantity=request.quantity,
            reserved=0,
        )

        product_id = self._repository.save(product)

        return product_id

    def get_product(self, product_id: int) -> Product | None:
        return self._repository.get_product(product_id)

    def reserve_product(self, product_id: int) -> None:
        reserved = self._repository.reserve_product(product_id)

        if reserved:
            return

        product = self._repository.get_product(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product does not exist",
            )

        raise HTTPException(
            status_code=400,
            detail="Product is sold out",
        )