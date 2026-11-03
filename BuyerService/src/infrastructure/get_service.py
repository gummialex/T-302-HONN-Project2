from functools import lru_cache

from src.infrastructure.buyer_repository import BuyerRepository
from src.services.buyer_service import BuyerService


@lru_cache
def get_buyer_service() -> BuyerService:
    return BuyerService(repository=BuyerRepository())