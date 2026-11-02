from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://orders:orders_dev_password@localhost:5432/orders"
    merchant_service_url: str = "http://localhost:8001"
    buyer_service_url: str = "http://localhost:8002"
    inventory_service_url: str = "http://localhost:8003"
    rabbitmq_url: str = "amqp://project:project_dev_password@localhost:5672/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"