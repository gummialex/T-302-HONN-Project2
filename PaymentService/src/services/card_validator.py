from src.dtos.process_payment_dto import CreditCardDTO


class CardValidator:

    def is_valid(self, card: CreditCardDTO) -> bool:
        if not self._valid_card_number(card.cardNumber):
            return False

        if not 1 <= card.expirationMonth <= 12:
            return False

        if not 1000 <= card.expirationYear <= 9999:
            return False

        if not 100 <= card.cvc <= 999:
            return False

        return True

    def _valid_card_number(self, card_number: str) -> bool:
        if len(card_number) < 2:
            return False

        if not all("0" <= character <= "9" for character in card_number):
            return False

        total = 0

        for index, character in enumerate(reversed(card_number)):
            digit = int(character)

            if index % 2 == 1:
                digit = digit * 2

                if digit > 9:
                    digit = digit - 9

            total = total + digit

        return total % 10 == 0