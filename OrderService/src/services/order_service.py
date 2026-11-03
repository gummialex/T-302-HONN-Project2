from fastapi import HTTPException

from dtos.create_order_dto import CreateOrder
from dtos.order_created_event import OrderCreatedEvent
from models.order import Order
from infrastructure.order_repository import OrderRepository
from infrastructure.merchant_client import MerchantClient
from infrastructure.buyer_client import BuyerClient
from infrastructure.inventory_client import InventoryClient
from infrastructure.event_publisher import EventPublisher


class OrderService:
    # DI
    def __init__(
        self,
        order_repository: OrderRepository,
        merchant_client: MerchantClient,
        buyer_client: BuyerClient,
        inventory_client: InventoryClient,
        event_publisher: EventPublisher
    ):
        self._repository = order_repository
        self._merchant_client = merchant_client
        self._buyer_client = buyer_client
        self._inventory_client = inventory_client
        self._event_publisher = event_publisher


    def create_order(self, request: CreateOrder) -> Order:
        merchant = self._merchant_client.get_merchant(request.merchantId)
        buyer = self._buyer_client.get_buyer(request.buyerId)
        product = self._inventory_client.get_product(request.productId)
        
        self._validate(request, merchant, buyer, product)

        total_price = product["price"] * (1 - (request.discount or 0))

        self._inventory_client.reserve(request.productId)

        order = Order(
            productId=request.productId,
            merchantId=request.merchantId,
            buyerId=request.buyerId,
            cardNumber=self._mask(request.creditCard.cardNumber),
            totalPrice=total_price,
        )
        stored = self._repository.save(order)

        event = OrderCreatedEvent(
            orderId=stored.id,
            productId=stored.productId,
            productName=product["productName"],
            merchantId=stored.merchantId,
            buyerId=stored.buyerId,
            totalPrice=stored.totalPrice,
            creditCard=request.creditCard.model_dump(), # model_dump converts the model instance into a dict
            buyerEmail=buyer["email"],
            merchantEmail=merchant["email"],
        )

        self._event_publisher.publish_order_created(event)
        return stored

    @staticmethod
    def _mask(card_number: str) -> str:
        last_digits = card_number[-4:]

        total_hidden = "*" * (len(card_number) - len(last_digits))

        return total_hidden + last_digits


    def get_order_by_id(self, order_id: int) -> Order:
        order = self._repository.get_order_by_id(order_id)

        if order is None:
            raise HTTPException(status_code=404, detail='Order does not exist')

        return order

    @staticmethod
    def _validate(request: CreateOrder, merchant: dict | None, buyer: dict | None, product: dict | None) -> None:
        if merchant is None:
            raise HTTPException(status_code=400, detail='Merchant does not exist')
        
        if buyer is None:
            raise HTTPException(status_code=400, detail='Buyer does not exist')
        
        if product is None:
            raise HTTPException(status_code=400, detail='Product does not exist')
        
        if product["quantity"] - product["reserved"] <= 0:
            raise HTTPException(status_code=400, detail='Product is sold out')
        
        if product["merchantId"] != request.merchantId:
            raise HTTPException(status_code=400, detail='Product does not belong to merchant')
        
        if request.discount and not merchant["allowsDiscount"]:
            raise HTTPException(status_code=400, detail='Merchant does not allow discount')