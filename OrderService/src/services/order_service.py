from fastapi import HTTPException
from OrderService.src.dtos.create_order_dto import CreateOrder
from OrderService.src.models.order import Order
from OrderService.src.infrastructure.order_repository import OrderDB
from OrderService.src.infrastructure.buyer_client import BuyerClient
from OrderService.src.infrastructure.inventory_client import InventoryClient
from OrderService.src.infrastructure.merchant_client import MerchantClient
from OrderService.src.infrastructure.event_publisher import EventPublisher
from OrderService.src.infrastructure.get_service import get_order_service




class OrderService:
    def __init__(self, order_repository: OrderDB, merchant_client: MerchantClient, buyer_client: BuyerClient, inventory_client: InventoryClient, event_publisher: EventPublisher):
        self._repository = order_repository
        self._merchant_client = merchant_client
        self._buyer_client = buyer_client
        self._inventory_client = inventory_client
        self._event_publisher = event_publisher

    def get_all_orders(self):   # ? do we need this
        # return all orders
        pass

    def create_order(self, request: CreateOrder) -> Order:

        self._validate(request)

        price = self._inventory_client.get_price(request.productId)
        total_price = price * (1 - (request.discount or 0))

        # Create the order
        order = Order(
            productId=request.productId,
            merchantId=request.merchantId,
            buyerId=request.buyerId,
            cardNumber=self.mask(request.creditCard.cardNumber),    # need mask for creditcard masking
            totalPrice=total_price
        )

        # Store the event in DB
        stored = self._repository.save(order)

        # Publishing the event with RabbitMQ
        self._event_publisher.publish_order_created(stored, request.creditCard)

        return stored


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