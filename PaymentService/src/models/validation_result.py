from dataclasses import dataclass

from src.models.payment_error import PaymentError


@dataclass(frozen=True)
class ValidationResult:
    error: PaymentError | None = None

    @property
    def successful(self) -> bool:
        return self.error is None