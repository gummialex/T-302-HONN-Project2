from functools import lru_cache

from src.infrastructure.repository import ProductRepository
from src.services.inventory_service import InventoryService


@lru_cache
def get_inventory_service() -> InventoryService:
    return InventoryService(repository=ProductRepository())