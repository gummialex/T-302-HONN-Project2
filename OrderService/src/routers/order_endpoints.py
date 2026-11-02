from  fastapi import APIRouter, Depends, status

from dtos.create_order_dto import CreateOrder
from infrastructure.get_service import get_order_service
from services.order_service import OrderService


router = APIRouter(prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED)
def create_order(request: CreateOrder, order_service: OrderService = Depends(get_order_service)):
    order = order_service.create_order(request)
    return order.id

@router.get('/{order_id}')
def get_orders(order_id: int, order_service: OrderService = Depends(get_order_service)):
    return order_service.get_order_by_id(order_id)