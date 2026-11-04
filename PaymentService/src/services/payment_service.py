from src.dtos.process_payment_dto import ProcessPaymentDTO
from src.infrastructure.payment_repository import PaymentRepository
from src.models.payment import Payment
from src.services.card_validator import CardValidator


class PaymentService:

    def __init__(
        self,
        repository: PaymentRepository,
        validator: CardValidator,
    ):
        self._repository = repository
        self._validator = validator

    def process_payment(self, request: ProcessPaymentDTO) -> Payment:
        existing_payment = self._repository.get_by_order_id(
            request.orderId
        )

        if existing_payment is not None:
            if existing_payment.productId != request.productId:
                raise ValueError(
                    "Order already has a payment for another product"
                )
            return existing_payment

        validation = self._validator.validate(request.creditCard)

        payment = Payment(
            orderId=request.orderId,
            productId=request.productId,
            error=validation.error,
        )

        return self._repository.save(payment)