from fastapi import APIRouter, Depends, Response

from infrastructure.get_service import get_order_proxy
from infrastructure.service_proxy import ServiceProxy

router = APIRouter(prefix="/api")


@router.get("/orders/{order_id}")
def get_order(order_id: int, proxy: ServiceProxy = Depends(get_order_proxy)) -> Response:
    return proxy.forward_get(f"/orders/{order_id}")


@router.post("/orders")
def create_order(body: dict, proxy: ServiceProxy = Depends(get_order_proxy)) -> Response:
    return proxy.forward_post("/orders", body)