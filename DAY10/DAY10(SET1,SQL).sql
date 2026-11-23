
CREATE DATABASE IF NOT EXISTS RetailPriceAuditDB;
USE RetailPriceAuditDB;

DROP TRIGGER IF EXISTS trg_price_before_update;
DROP TRIGGER IF EXISTS trg_price_after_update;
DROP PROCEDURE IF EXISTS usp_UpdateProductPrice;

DROP TABLE IF EXISTS rejected_price_attempts;
DROP TABLE IF EXISTS price_audit;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE price_audit (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    changed_by VARCHAR(100),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE rejected_price_attempts (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    attempted_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    attempted_by VARCHAR(100),
    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products
(product_name, cost_price, product_price)
VALUES
('Laptop', 40000, 50000),
('Mouse', 300, 500),
('Keyboard', 800, 1200),
('Monitor', 9000, 12000),
('Headphones', 1000, 1500);

DELIMITER //

CREATE TRIGGER trg_price_before_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    IF NEW.product_price < NEW.cost_price THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price cannot be below cost price';
    END IF;
END //

CREATE TRIGGER trg_price_after_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    IF OLD.product_price <> NEW.product_price THEN
        INSERT INTO price_audit
        (product_id, old_price, new_price, changed_by, changed_at)
        VALUES
        (NEW.product_id, OLD.product_price, NEW.product_price,
         CURRENT_USER(), NOW());
    END IF;
END //

CREATE PROCEDURE usp_UpdateProductPrice(
    IN p_product_id INT,
    IN p_new_price DECIMAL(10,2)
)
BEGIN
    DECLARE v_cost_price DECIMAL(10,2);
    DECLARE v_exists INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_exists
    FROM products
    WHERE product_id = p_product_id;

    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product not found';
    END IF;

    SELECT cost_price INTO v_cost_price
    FROM products
    WHERE product_id = p_product_id
    FOR UPDATE;

    IF p_new_price < v_cost_price THEN

        INSERT INTO rejected_price_attempts
        (product_id, attempted_price, cost_price,
         attempted_by, reason)
        VALUES
        (p_product_id, p_new_price, v_cost_price,
         CURRENT_USER(), 'Price below cost price');

        COMMIT;

        SELECT 'Price rejected' AS Result;

    ELSE

        UPDATE products
        SET product_price = p_new_price
        WHERE product_id = p_product_id;

        COMMIT;

        SELECT 'Price updated successfully' AS Result;

    END IF;
END //

DELIMITER ;

UPDATE products
SET product_price = 52000
WHERE product_id = 1;

UPDATE products
SET product_price = product_price + 100
WHERE product_id IN (2, 3, 4);

CALL usp_UpdateProductPrice(1, 30000);

CALL usp_UpdateProductPrice(2, 700);

SELECT * FROM products;
SELECT * FROM price_audit;
SELECT * FROM rejected_price_attempts;
