from src.infrastructure.repository import ProductRepository
from src.services.inventory_service import InventoryService


product_repository = ProductRepository()

inventory_service = InventoryService(product_repository)