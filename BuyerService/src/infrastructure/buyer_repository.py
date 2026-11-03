from src.dtos.buyer_dto import Buyer
from src.infrastructure.database import get_connection


class BuyerRepository:

    def save_buyer(self, buyer: Buyer) -> int:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO buyers
                        (name, ssn, email, phone_number)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        buyer.name,
                        buyer.ssn,
                        buyer.email,
                        buyer.phoneNumber
                    )
                )

                buyer_id = cursor.fetchone()[0]

        return buyer_id

    def get_buyer(self, buyer_id: int) -> Buyer | None:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT name, ssn, email, phone_number
                    FROM buyers
                    WHERE id = %s
                    """,
                    (buyer_id,)
                )

                result = cursor.fetchone()

        if result is None:
            return None

        return Buyer(
            name=result[0],
            ssn=result[1],
            email=result[2],
            phoneNumber=result[3]
        )
