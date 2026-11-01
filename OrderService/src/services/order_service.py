from fastapi import HTTPException
from dtos.create_order_dto import CreateOrder
from models.order import Order
from infrastructure.order_repository import OrderDB



class OrderService:
    def __init__(self):
        self.orders = "ordersDB"
        self.next_id =  1 # vantar logic fyrir id?

    def get_all_orders(self) -> list[Order]:
        # return all orders
        pass

    def create_order(self, request: CreateOrder) -> Order:
        # reserve order
        # store order
        # publish event
        pass

    def _validate(self, request: CreateOrder) -> None:
        if not self._merchant_exists(request.merchantId):
            raise HTTPException(status_code=400, detail='Merchant does not exist')
        
        if not self._buyer_exists(request.buyerId):
            raise HTTPException(status_code=400, detail='Buyer does not exist')
        
        if not self._product_exists(request.productId):
            raise HTTPException(status_code=400, detail='Product does not exist')
        
        if not self._product_in_stock(request.productId):
            raise HTTPException(status_code=400, detail='Product is sold out')
        
        if not self._product_belongs_to_merchant(request.productId, request.merchantId):
            raise HTTPException(status_code=400, detail='Product does not belong to merchant')
        
        if request.discount and not self._merchant_allows_discount(request.merchantId):
            raise HTTPException(status_code=400, detail='Merchant does not allow discount')
        

    def _merchant_exists(self, merchant_id: int) -> bool:
        # kalla í MerchantService
        pass

    def _buyer_exists(self, buyer_id: int) -> bool:
        # kalla í OrderDB sem kallar í BuyerService ?
        pass

    def _product_exists(self, product_id: int) -> bool:
        # kalla í InventoryService
        pass

    def _product_in_stock(self, product_id: int) -> bool:
        # kalla í InventoryService
        pass

    def _product_belongs_to_merchant(self, product_id: int, merchant_id: int) -> bool:
        # kalla í InventoryService
        pass

    def _merchant_allows_discount(self, merchant_id: int) -> bool:
        # Kalla i MerchantService
        pass