from fastapi import HTTPException
from dtos.create_order_dto import CreateOrder
from models.order import Order


class OrderService:
    def __init__(self):
        self.orders: list[Order] = []
        self.next_id = 1    # ???

    def get_all_orders(self) -> list[Order]:
        return self.orders

    def create_order(self, request: CreateOrder) -> Order:
        pass

    def _validate(self, request: CreateOrder) -> None:
        if not self._merchant_exists(request.merchantID):
            raise HTTPException(status_code=400, detail='Merchant does not exist')
        
        if not self._buyer_exists(request.buyerID):
            raise HTTPException(status_code=400, detail='Merchant does not exist')
        
        if not self._merchant_exists(request.merchantID):
            raise HTTPException(status_code=400, detail='Merchant does not exist')

    def _merchant_exists(self, merchant_id: int) -> bool:
        # kalla í MerchantService
        pass

    def _buyer_exists(self, buyer_id: int) -> bool:
        # kalla í BuyerService
        pass
