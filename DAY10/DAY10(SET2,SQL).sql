
CREATE DATABASE IF NOT EXISTS BankBalanceGuardDB;
USE BankBalanceGuardDB;

DROP VIEW IF EXISTS vw_savings_accounts;
DROP PROCEDURE IF EXISTS usp_TestBatchUpdate;

DROP TRIGGER IF EXISTS trg_transaction_insert;
DROP TRIGGER IF EXISTS trg_transaction_update;
DROP TRIGGER IF EXISTS trg_transaction_delete;
DROP TRIGGER IF EXISTS trg_prevent_negative_balance;

DROP TABLE IF EXISTS transaction_audit;
DROP TABLE IF EXISTS account_transaction;
DROP TABLE IF EXISTS accounts;


-- TABLE CREATION

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    account_holder VARCHAR(100),
    account_type VARCHAR(30),
    balance DECIMAL(12,2) NOT NULL
);

CREATE TABLE account_transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    transaction_type VARCHAR(30),
    amount DECIMAL(12,2),
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transaction_audit (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT,
    action_type VARCHAR(20),
    old_account_id INT,
    new_account_id INT,
    old_amount DECIMAL(12,2),
    new_amount DECIMAL(12,2),
    changed_by VARCHAR(100),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- SAMPLE DATA

INSERT INTO accounts VALUES
(1, 'Arun', 'Savings', 10000),
(2, 'Rahul', 'Savings', 8000),
(3, 'Kumar', 'Savings', 5000),
(4, 'Vijay', 'Savings', 12000),
(5, 'Ajay', 'Current', 15000);

INSERT INTO account_transaction
(account_id, transaction_type, amount)
VALUES
(1, 'Deposit', 2000),
(2, 'Withdrawal', 1000),
(3, 'Deposit', 3000),
(4, 'Withdrawal', 2000),
(5, 'Deposit', 5000);


-- TASK 1: AFTER INSERT TRIGGER

DELIMITER //

CREATE TRIGGER trg_transaction_insert
AFTER INSERT ON account_transaction
FOR EACH ROW
BEGIN
    INSERT INTO transaction_audit
    (transaction_id, action_type, new_account_id,
     new_amount, changed_by, changed_at)
    VALUES
    (NEW.transaction_id, 'INSERT', NEW.account_id,
     NEW.amount, CURRENT_USER(), NOW());
END //


-- AFTER UPDATE TRIGGER

CREATE TRIGGER trg_transaction_update
AFTER UPDATE ON account_transaction
FOR EACH ROW
BEGIN
    INSERT INTO transaction_audit
    (transaction_id, action_type,
     old_account_id, new_account_id,
     old_amount, new_amount, changed_by, changed_at)
    VALUES
    (NEW.transaction_id, 'UPDATE',
     OLD.account_id, NEW.account_id,
     OLD.amount, NEW.amount, CURRENT_USER(), NOW());
END //


-- AFTER DELETE TRIGGER

CREATE TRIGGER trg_transaction_delete
AFTER DELETE ON account_transaction
FOR EACH ROW
BEGIN
    INSERT INTO transaction_audit
    (transaction_id, action_type, old_account_id,
     old_amount, changed_by, changed_at)
    VALUES
    (OLD.transaction_id, 'DELETE', OLD.account_id,
     OLD.amount, CURRENT_USER(), NOW());
END //

DELIMITER ;


-- TEST INSERT

INSERT INTO account_transaction
(account_id, transaction_type, amount)
VALUES (1, 'Deposit', 500);


-- TEST UPDATE

UPDATE account_transaction
SET amount = 2500
WHERE transaction_id = 1;


-- TEST DELETE

DELETE FROM account_transaction
WHERE transaction_id = 5;


-- TASK 2: CREATE SAVINGS ACCOUNT VIEW

CREATE VIEW vw_savings_accounts AS
SELECT
    account_id,
    account_holder,
    balance
FROM accounts
WHERE account_type = 'Savings';


-- DISPLAY VIEW

SELECT * FROM vw_savings_accounts;


-- MYSQL EQUIVALENT OF INSTEAD OF UPDATE
-- MySQL does not support INSTEAD OF triggers.
-- Use a BEFORE UPDATE trigger on the base table.

DELIMITER //

CREATE TRIGGER trg_prevent_negative_balance
BEFORE UPDATE ON accounts
FOR EACH ROW
BEGIN
    IF NEW.account_type = 'Savings'
       AND NEW.balance < 0 THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Error: Savings balance cannot be negative';

    END IF;
END //

DELIMITER ;


-- TEST VALID UPDATE THROUGH VIEW

UPDATE vw_savings_accounts
SET balance = 11000
WHERE account_id = 1;


-- TASK 3: BATCH UPDATE OF FIVE ACCOUNTS
-- One account violates the negative balance rule.
-- Entire statement should be rejected.

DELIMITER //

CREATE PROCEDURE usp_TestBatchUpdate()
BEGIN

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Batch update rejected. No changes committed.'
        AS Result;
    END;

    START TRANSACTION;

    UPDATE accounts
    SET balance = CASE account_id
        WHEN 1 THEN 12000
        WHEN 2 THEN 9000
        WHEN 3 THEN -500
        WHEN 4 THEN 14000
        WHEN 5 THEN 16000
        ELSE balance
    END
    WHERE account_id IN (1,2,3,4,5);

    COMMIT;

    SELECT 'Batch update successful' AS Result;

END //

DELIMITER ;


CALL usp_TestBatchUpdate();


-- VERIFY ACCOUNT BALANCES

SELECT * FROM accounts;


-- TASK 4: NESTED AND RECURSIVE TRIGGER EXPLANATION
-- Nested triggers occur when one trigger operation
-- activates another trigger.
-- Recursive triggers occur when trigger actions
-- cause the same trigger to execute again.
-- Prevent loops by avoiding updates to the same
-- triggering table and using explicit conditions.
-- Keep trigger dependencies simple.


-- FINAL AUDIT VERIFICATION

SELECT * FROM transaction_audit;

SELECT * FROM account_transaction;

SELECT * FROM vw_savings_accounts;
