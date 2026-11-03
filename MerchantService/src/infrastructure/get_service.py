from functools import lru_cache

from infrastructure.settings import Settings
from infrastructure.merchant_repository import MerchantRepository
from services.merchant_service import MerchantService


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_merchant_service() -> MerchantService:
    settings = get_settings()

    return MerchantService(repository=MerchantRepository(settings.database_url))