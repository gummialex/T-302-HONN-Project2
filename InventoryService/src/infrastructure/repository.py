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

    def reserve_product(self, product_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET reserved = reserved + 1
                    WHERE id = %s
                    AND quantity > reserved
                    RETURNING id
                    """,
                    (product_id,),
                )

                result = cursor.fetchone()

        return result is not None