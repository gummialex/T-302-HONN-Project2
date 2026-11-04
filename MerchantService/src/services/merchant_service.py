from src.dtos.merchant_dto import Merchant
from src.infrastructure.merchant_repository import MerchantRepository


class MerchantService:
    def __init__(self, repository: MerchantRepository):
        self.__repository = repository

    def create_merchant(self, merchant: Merchant) -> int:
        merchant_id = self.__repository.save_merchant(merchant)

        return merchant_id

    def get_merchant(self, id: int) -> Merchant:
        merchant = self.__repository.get_merchant(id)

        return merchant