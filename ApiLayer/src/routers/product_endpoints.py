from fastapi import APIRouter, Depends, Response

from infrastructure.get_service import get_inventory_proxy
from infrastructure.service_proxy import ServiceProxy

router = APIRouter(prefix="/api")


@router.get("/products/{product_id}")
def get_product(product_id: int, proxy: ServiceProxy = Depends(get_inventory_proxy)) -> Response:
    return proxy.forward_get(f"/products/{product_id}")


@router.post("/products")
def create_product(body: dict, proxy: ServiceProxy = Depends(get_inventory_proxy)) -> Response:
    return proxy.forward_post("/products", body)