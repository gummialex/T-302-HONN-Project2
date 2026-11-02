from fastapi import HTTPException

from dtos.create_order_dto import CreateOrder
from models.order import Order
from infrastructure.order_repository import OrderRepository



class OrderService:
    def __init__(self, order_repository: OrderRepository):  # DPI
        self._repository = order_repository


    def create_order(self, request: CreateOrder) -> Order:
        
        self._validate(request)

        total_price = 0.0 # TODO: get the price from InventoryService

        order = Order(
            productId=request.productId,
            merchantId=request.merchantId,
            buyerId=request.buyerId,
            cardNumber=request.creditCard.cardNumber,    # TODO: mask for credit card
            totalPrice=total_price,
        )

        return self._repository.save(order)

    def get_order_by_id(self, order_id: int) -> Order:
        order = self._repository.get_by_id(order_id)

        if order is None:
            raise HTTPException(status_code=404, detail='Order does not exist')

        return order


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
        # TODO: kalla i MerchantService
        return True

    def _buyer_exists(self, buyer_id: int) -> bool:
        # TODO: kalla i BuyerService
        return True

    def _product_exists(self, product_id: int) -> bool:
        # TODO: kalla i InventoryService
        return True

    def _product_in_stock(self, product_id: int) -> bool:
        # TODO: kalla i InventoryService
        return True

    def _product_belongs_to_merchant(self, product_id: int, merchant_id: int) -> bool:
        # TODO: kalla i InventoryService
        return True

    def _merchant_allows_discount(self, merchant_id: int) -> bool:
        # TODO: kalla i MerchantService
        return True