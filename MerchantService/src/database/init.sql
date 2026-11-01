
CREATE TABLE IF NOT EXISTS merchants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ssn VARCHAR(10) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(30) NOT NULL,
    allows_discount BOOLEAN NOT NULL
);
