from src.models.product import Product
from src.infrastructure.database import get_connection


class ProductRepository:

    def save(self, product: Product) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products
                        (merchantId, productName, price, quantity, reserved)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        product.merchantId,
                        product.productName,
                        product.price,
                        product.quantity,
                        product.reserved,
                    ),
                )

                product_id = cursor.fetchone()[0]

        return product_id

    def get_product(self, product_id: int) -> Product | None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        merchantId,
                        productName,
                        price,
                        quantity,
                        reserved,
                        id
                    FROM products
                    WHERE id = %s
                    """,
                    (product_id,),
                )

                result = cursor.fetchone()

        if result is None:
            return None

        return Product(
            merchantId=result[0],
            productName=result[1],
            price=result[2],
            quantity=result[3],
            reserved=result[4],
            id=result[5],
        )

    def reserve_product(
        self,
        product_id: int,
        order_id: int,
    ) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT quantity, reserved
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (product_id,),
                )

                product = cursor.fetchone()

                if product is None:
                    return False

                cursor.execute(
                    """
                    SELECT product_id
                    FROM reservations
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )

                existing = cursor.fetchone()

                if existing is not None:
                    if existing[0] != product_id:
                        raise ValueError(
                            "Order already reserved another product"
                        )

                    return True

                quantity, reserved = product

                if quantity <= reserved:
                    return False

                cursor.execute(
                    """
                    INSERT INTO reservations (order_id, product_id)
                    VALUES (%s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                    RETURNING order_id
                    """,
                    (order_id, product_id),
                )

                if cursor.fetchone() is None:
                    raise ValueError(
                        "Order already has another reservation"
                    )

                cursor.execute(
                    """
                    UPDATE products
                    SET reserved = reserved + 1
                    WHERE id = %s
                    """,
                    (product_id,),
                )

        return True

    def apply_payment_result(
        self,
        order_id: int,
        product_id: int,
        successful: bool,
    ) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT product_id, successful
                    FROM reservations
                    WHERE order_id = %s
                    FOR UPDATE
                    """,
                    (order_id,),
                )

                reservation = cursor.fetchone()

                if reservation is None:
                    raise ValueError("Reservation does not exist")

                stored_product_id, previous_result = reservation

                if stored_product_id != product_id:
                    raise ValueError(
                        "Payment product does not match reservation"
                    )

                if previous_result is not None:
                    if previous_result != successful:
                        raise ValueError(
                            "Reservation already has a different result"
                        )

                    return

                if successful:
                    cursor.execute(
                        """
                        UPDATE products
                        SET quantity = quantity - 1,
                            reserved = reserved - 1
                        WHERE id = %s
                        AND reserved > 0
                        """,
                        (product_id,),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE products
                        SET reserved = reserved - 1
                        WHERE id = %s
                          AND reserved > 0
                        """,
                        (product_id,),
                    )

                if cursor.rowcount != 1:
                    raise ValueError(
                        "Product reservation count is inconsistent"
                    )

                cursor.execute(
                    """
                    UPDATE reservations
                    SET successful = %s
                    WHERE order_id = %s
                    """,
                    (successful, order_id),
                )