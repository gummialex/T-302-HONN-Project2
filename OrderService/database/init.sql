CREATE TABLE IF NOT EXISTS orders (
    id           SERIAL PRIMARY KEY,
    product_id   INTEGER NOT NULL,
    merchant_id  INTEGER NOT NULL,
    buyer_id     INTEGER NOT NULL,
    card_number  TEXT NOT NULL,
    total_price  DOUBLE PRECISION NOT NULL
);