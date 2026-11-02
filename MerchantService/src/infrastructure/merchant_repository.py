
from src.dtos.merchant_dto import Merchant
from src.infrastructure.database import get_connection


class MerchantRepository:

    def save_merchant(self, merchant: Merchant) -> int:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO merchants
                        (name, ssn, email, phone_number, allows_discount)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        merchant.name,
                        merchant.ssn,
                        merchant.email,
                        merchant.phoneNumber,
                        merchant.allowsDiscount
                    )
                )

                merchant_id = cursor.fetchone()[0]

        return merchant_id

    def get_merchant(self, merchant_id: int) -> Merchant | None:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT name, ssn, email, phone_number, allows_discount
                    FROM merchants
                    WHERE id = %s
                    """,
                    (merchant_id,)
                )

                result = cursor.fetchone()

        if result is None:
            return None

        return Merchant(
            name=result[0],
            ssn=result[1],
            email=result[2],
            phoneNumber=result[3],
            allowsDiscount=result[4]
        )
