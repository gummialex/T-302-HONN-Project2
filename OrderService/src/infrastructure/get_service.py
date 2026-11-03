"""Dependency wiring.

The only place that chooses concrete implementations. Change what
OrderService talks to by editing here, not by editing the service.
"""

from functools import lru_cache

from infrastructure.settings import Settings
from infrastructure.order_repository import OrderRepository
from infrastructure.merchant_client import MerchantClient
from infrastructure.buyer_client import BuyerClient
from infrastructure.inventory_client import InventoryClient
from infrastructure.event_publisher import EventPublisher
from services.order_service import OrderService


@lru_cache
def get_settings() -> Settings:
    return Settings()

@lru_cache
def get_order_service() -> OrderService:
    """Builds the OrderService once per process

    Cached because Depends() runs this on every request, without it
    each request would open a new connection pool and exhaust Postgres
    """

    settings = get_settings()

    return OrderService(
        order_repository=OrderRepository(settings.database_url),
        merchant_client=MerchantClient(settings.merchant_service_url),
        buyer_client=BuyerClient(settings.buyer_service_url),
        inventory_client=InventoryClient(settings.inventory_service_url),
        event_publisher=EventPublisher(settings.rabbitmq_url),
    )