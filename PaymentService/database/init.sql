CREATE TABLE IF NOT EXISTS payments (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    successful BOOLEAN NOT NULL,
    error_code TEXT,
    CHECK (
        (successful = TRUE AND error_code IS NULL)
        OR
        (successful = FALSE AND error_code IS NOT NULL)
    )
);