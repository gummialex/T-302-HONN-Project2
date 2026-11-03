from functools import lru_cache

from src.infrastructure.settings import Settings
from src.infrastructure.merchant_repository import MerchantRepository
from src.services.merchant_service import MerchantService


@lru_cache
def get_merchant_service() -> MerchantService:

    return MerchantService(repository=MerchantRepository())