from src.dtos.buyer_dto import Buyer
from src.infrastructure.buyer_repository import BuyerRepository


class BuyerService:
    def __init__(self):
        self.__repository = BuyerRepository()

    def create_buyer(self, buyer: Buyer) -> int:
        buyer_id = self.__repository.save_buyer(buyer)

        return buyer_id

    def get_buyer(self, id: int) -> Buyer:
        buyer = self.__repository.get_buyer(id)

        return buyer