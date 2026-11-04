from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from models.order import Order


class OrderRepository:

    def __init__(self, database_url: str):
        # Opening a connection to Postgres
        self._pool = ConnectionPool(database_url,min_size=1, max_size=5, open=True)

    def save(self, order: Order) -> Order:
        if order.id is None:
            raise ValueError("Order ID must be allocated before saving")

        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO orders (
                        id,
                        product_id,
                        merchant_id,
                        buyer_id,
                        card_number,
                        total_price
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        order.id,
                        order.productId,
                        order.merchantId,
                        order.buyerId,
                        order.cardNumber,
                        order.totalPrice,
                    ),
                )

        return order

    def get_order_by_id(self, order_id: int) -> Order | None:
        """Returns order by id"""

        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT id, product_id, merchant_id, buyer_id, card_number, total_price
                    FROM orders
                    WHERE id = %s
                    """,
                    (order_id,),
                )
                row = cursor.fetchone()

        if row is None:
            return None

        return self._to_order(row)


    @staticmethod
    def _to_order(row: dict) -> Order:
        return Order(
            productId=row["product_id"],
            merchantId=row["merchant_id"],
            buyerId=row["buyer_id"],
            cardNumber=row["card_number"],
            totalPrice=row["total_price"],
            id=row["id"]
        )

    def allocate_id(self) -> int:
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT nextval(pg_get_serial_sequence('orders', 'id'))"
                )
                return cursor.fetchone()[0]
