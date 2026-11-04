from datetime import date

from src.dtos.process_payment_dto import CreditCardDTO
from src.models.payment_error import PaymentError
from src.models.validation_result import ValidationResult


class CardValidator:

    def validate(self, card: CreditCardDTO) -> ValidationResult:
        if not self._valid_card_number(card.cardNumber):
            return ValidationResult(
                error=PaymentError.INVALID_CARD_NUMBER
            )

        if not self._valid_month(card.expirationMonth):
            return ValidationResult(
                error=PaymentError.INVALID_EXPIRATION_MONTH
            )

        if not self._valid_year(card.expirationYear):
            return ValidationResult(
                error=PaymentError.INVALID_EXPIRATION_YEAR
            )

        if self._expired(
            card.expirationYear,
            card.expirationMonth,
        ):
            return ValidationResult(
                error=PaymentError.CARD_EXPIRED
            )

        if not self._valid_cvc(card.cvc):
            return ValidationResult(
                error=PaymentError.INVALID_CVC
            )

        return ValidationResult()

    def _valid_month(self, month: int) -> bool:
        return 1 <= month <= 12

    def _valid_year(self, year: int) -> bool:
        return 1000 <= year <= 9999

    def _expired(self, year: int, month: int) -> bool:
        today = date.today()

        return (year, month) < (today.year, today.month)

    def _valid_cvc(self, cvc: str) -> bool:
        return (
            len(cvc) == 3
            and all("0" <= character <= "9" for character in cvc)
        )

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