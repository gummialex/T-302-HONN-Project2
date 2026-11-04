from src.infrastructure.payment_repository import PaymentRepository
from src.services.card_validator import CardValidator
from src.services.payment_service import PaymentService


payment_repository = PaymentRepository()
card_validator = CardValidator()

payment_service = PaymentService(
    repository=payment_repository,
    validator=card_validator,
)