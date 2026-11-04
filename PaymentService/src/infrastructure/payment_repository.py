from src.infrastructure.database import get_connection
from src.models.payment import Payment
from src.models.payment_error import PaymentError


class PaymentRepository:

    def save(self, payment: Payment) -> Payment:
        error_code = (
            payment.error.value
            if payment.error is not None
            else None
        )

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO payments (
                        order_id,
                        product_id,
                        successful,
                        error_code
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                    """,
                    (
                        payment.orderId,
                        payment.productId,
                        payment.successful,
                        error_code,
                    ),
                )

                cursor.execute(
                    """
                    SELECT order_id, product_id, error_code
                    FROM payments
                    WHERE order_id = %s 
                    """,
                    (payment.orderId,),
                )

                row = cursor.fetchone()

        stored_payment = self._to_payment(row)

        if stored_payment.productId != payment.productId:
            raise ValueError(
                "Order already has a payment for another product"
            )

        return stored_payment

    def get_by_order_id(self, order_id: int) -> Payment | None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT order_id, product_id, error_code
                    FROM payments
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return self._to_payment(row)

    def _to_payment(self, row) -> Payment:
        error = (
            PaymentError(row[2])
            if row[2] is not None
            else None
        )

        return Payment(
            orderId=row[0],
            productId=row[1],
            error=error,
        )