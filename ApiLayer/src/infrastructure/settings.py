from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    order_service_url: str = "http://localhost:8000"
    merchant_service_url: str = "http://localhost:8001"
    buyer_service_url: str = "http://localhost:8002"
    inventory_service_url: str = "http://localhost:8003"