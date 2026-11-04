from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://merchant:merchant_dev_password@localhost:5432/merchants"