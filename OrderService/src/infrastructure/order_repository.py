from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from OrderService.src.models.order import Order


class OrderRepository:

    def __init__(self, database_url: str):
        # Opening a connection to Postgres
        self._pool = ConnectionPool(database_url,min_size=1, max_size=5, open=True)

    def save(self, order: Order) -> Order:
        """Inserts the order and sets its database-assigned id.

        Mutates the order passed in and returns the same object.
        """

        with self._pool.connection() as conn:   # Take a connection out of the pool
            # Cursor is the obj that runs a statement and holds its result set
            with conn.cursor(row_factory=dict_row) as cursor:

                cursor.execute(
                    """
                    INSERT INTO orders (product_id, merchant_id, buyer_id, card_number, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        order.productId,
                        order.merchantId,
                        order.buyerId,
                        order.cardNumber,
                        order.totalPrice
                    )
                )
                row = cursor.fetchone() # pulls a single row from the result set. In this case: RETURNING id
        order.id = row["id"]
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
