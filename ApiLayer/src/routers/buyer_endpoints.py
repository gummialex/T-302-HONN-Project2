from fastapi import APIRouter, Depends, Response

from infrastructure.get_service import get_buyer_proxy
from infrastructure.service_proxy import ServiceProxy

router = APIRouter(prefix="/api")


@router.get("/buyers/{buyer_id}")
def get_buyer(buyer_id: int, proxy: ServiceProxy = Depends(get_buyer_proxy)) -> Response:
    return proxy.forward_get(f"/buyers/{buyer_id}")


@router.post("/buyers")
def create_buyer(body: dict, proxy: ServiceProxy = Depends(get_buyer_proxy)) -> Response:
    return proxy.forward_post("/buyers", body)