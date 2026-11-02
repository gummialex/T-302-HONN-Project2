from  fastapi import APIrouter, Depends, status

from InventoryService.src.dtos.product_dto import CreateProductDTO


@router.post('/products')
def create_product(dto: CreateProductDTO):
    pass

@router.get('/products/{id}')
def post_product(id: int):
    pass

@router.post('/products/{id}/reserve')
def reserve_product(id: int):
    pass
