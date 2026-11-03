CREATE TABLE IF NOT EXISTS products (
    merchantId INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    reserved INT,
    id INT PRIMARY KEY
);
