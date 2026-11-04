from functools import lru_cache

from infrastructure.service_proxy import ServiceProxy
from infrastructure.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_order_proxy() -> ServiceProxy:
    return ServiceProxy(get_settings().order_service_url)


@lru_cache
def get_merchant_proxy() -> ServiceProxy:
    return ServiceProxy(get_settings().merchant_service_url)


@lru_cache
def get_buyer_proxy() -> ServiceProxy:
    return ServiceProxy(get_settings().buyer_service_url)


@lru_cache
def get_inventory_proxy() -> ServiceProxy:
    return ServiceProxy(get_settings().inventory_service_url)