from fastapi import APIRouter, Depends, Response

from infrastructure.get_service import get_merchant_proxy
from infrastructure.service_proxy import ServiceProxy

router = APIRouter(prefix="/api")


@router.get("/merchants/{merchant_id}")
def get_merchant(merchant_id: int, proxy: ServiceProxy = Depends(get_merchant_proxy)) -> Response:
    return proxy.forward_get(f"/merchants/{merchant_id}")


@router.post("/merchants")
def create_merchant(body: dict, proxy: ServiceProxy = Depends(get_merchant_proxy)) -> Response:
    return proxy.forward_post("/merchants", body)