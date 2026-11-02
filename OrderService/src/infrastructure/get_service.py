"""Dependency wiring.

The only place that chooses concrete implementations. Change what
OrderService talks to by editing here, not by editing the service.
"""

from functools import lru_cache

from OrderService.src.infrastructure.settings import Settings
from OrderService.src.infrastructure.order_repository import OrderRepository
from OrderService.src.services.order_service import OrderService


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
    return OrderService(order_repository=OrderRepository(settings.database_url))
    
