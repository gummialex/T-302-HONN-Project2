CREATE TABLE IF NOT EXISTS products (
    merchantId INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL CHECK (price >= 0),
    quantity INT NOT NULL CHECK (quantity >= 0),
    reserved INT NOT NULL DEFAULT 0,
    id SERIAL PRIMARY KEY,
    CHECK (reserved >= 0 AND reserved <= quantity)
);

CREATE TABLE IF NOT EXISTS reservations (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    successful BOOLEAN
);
