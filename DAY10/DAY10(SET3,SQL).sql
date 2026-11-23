
CREATE DATABASE IF NOT EXISTS HospitalBedDB;
USE HospitalBedDB;

DROP PROCEDURE IF EXISTS usp_TestMultiRowAdmission;

DROP TRIGGER IF EXISTS trg_check_bed_insert;
DROP TRIGGER IF EXISTS trg_check_bed_update;
DROP TRIGGER IF EXISTS trg_admission_insert;
DROP TRIGGER IF EXISTS trg_admission_update;
DROP TRIGGER IF EXISTS trg_admission_delete;

DROP TABLE IF EXISTS admission_audit;
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS wards;


-- TABLE CREATION

CREATE TABLE wards (
    ward_id INT PRIMARY KEY,
    ward_name VARCHAR(100),
    bed_capacity INT NOT NULL
);

CREATE TABLE admissions (
    admission_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_name VARCHAR(100) NOT NULL,
    ward_id INT NOT NULL,
    admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'Admitted',
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);

CREATE TABLE admission_audit (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    admission_id INT,
    action_type VARCHAR(20),
    old_patient_name VARCHAR(100),
    new_patient_name VARCHAR(100),
    old_ward_id INT,
    new_ward_id INT,
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100)
);


-- SAMPLE DATA

INSERT INTO wards VALUES
(1, 'General Ward', 3),
(2, 'ICU', 2),
(3, 'Emergency Ward', 4);

INSERT INTO admissions
(patient_name, ward_id, status)
VALUES
('Arun', 1, 'Admitted'),
('Rahul', 1, 'Admitted'),
('Kumar', 2, 'Admitted');


-- TASK 1: BEFORE INSERT TRIGGER
-- Prevent admission when ward is full

DELIMITER //

CREATE TRIGGER trg_check_bed_insert
BEFORE INSERT ON admissions
FOR EACH ROW
BEGIN
    DECLARE v_capacity INT;
    DECLARE v_occupied INT;

    SELECT bed_capacity
    INTO v_capacity
    FROM wards
    WHERE ward_id = NEW.ward_id
    FOR UPDATE;

    SELECT COUNT(*)
    INTO v_occupied
    FROM admissions
    WHERE ward_id = NEW.ward_id
    AND status = 'Admitted';

    IF NEW.status = 'Admitted'
       AND v_occupied >= v_capacity THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Admission rejected: Ward is at full capacity';

    END IF;
END //


-- PREVENT OVERCAPACITY DURING UPDATE

CREATE TRIGGER trg_check_bed_update
BEFORE UPDATE ON admissions
FOR EACH ROW
BEGIN
    DECLARE v_capacity INT;
    DECLARE v_occupied INT;

    IF NEW.status = 'Admitted' THEN

        SELECT bed_capacity
        INTO v_capacity
        FROM wards
        WHERE ward_id = NEW.ward_id
        FOR UPDATE;

        SELECT COUNT(*)
        INTO v_occupied
        FROM admissions
        WHERE ward_id = NEW.ward_id
        AND status = 'Admitted'
        AND admission_id <> OLD.admission_id;

        IF v_occupied >= v_capacity THEN

            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
            'Update rejected: Ward has no available beds';

        END IF;

    END IF;
END //


-- TASK 2: AFTER INSERT TRIGGER

CREATE TRIGGER trg_admission_insert
AFTER INSERT ON admissions
FOR EACH ROW
BEGIN
    INSERT INTO admission_audit
    (
        admission_id,
        action_type,
        new_patient_name,
        new_ward_id,
        new_status,
        changed_at,
        changed_by
    )
    VALUES
    (
        NEW.admission_id,
        'INSERT',
        NEW.patient_name,
        NEW.ward_id,
        NEW.status,
        NOW(),
        CURRENT_USER()
    );
END //


-- AFTER UPDATE TRIGGER

CREATE TRIGGER trg_admission_update
AFTER UPDATE ON admissions
FOR EACH ROW
BEGIN
    INSERT INTO admission_audit
    (
        admission_id,
        action_type,
        old_patient_name,
        new_patient_name,
        old_ward_id,
        new_ward_id,
        old_status,
        new_status,
        changed_at,
        changed_by
    )
    VALUES
    (
        NEW.admission_id,
        'UPDATE',
        OLD.patient_name,
        NEW.patient_name,
        OLD.ward_id,
        NEW.ward_id,
        OLD.status,
        NEW.status,
        NOW(),
        CURRENT_USER()
    );
END //


-- AFTER DELETE TRIGGER

CREATE TRIGGER trg_admission_delete
AFTER DELETE ON admissions
FOR EACH ROW
BEGIN
    INSERT INTO admission_audit
    (
        admission_id,
        action_type,
        old_patient_name,
        old_ward_id,
        old_status,
        changed_at,
        changed_by
    )
    VALUES
    (
        OLD.admission_id,
        'DELETE',
        OLD.patient_name,
        OLD.ward_id,
        OLD.status,
        NOW(),
        CURRENT_USER()
    );
END //

DELIMITER ;


-- TASK 3: TEST INSERT

INSERT INTO admissions
(patient_name, ward_id, status)
VALUES
('Vijay', 1, 'Admitted');


-- TEST UPDATE

UPDATE admissions
SET patient_name = 'Vijay Kumar'
WHERE admission_id = 4;


-- TEST DELETE

DELETE FROM admissions
WHERE admission_id = 4;


-- MULTI-ROW INSERT TEST
-- General Ward has capacity 3 and currently 2 occupied beds.
-- Two new admissions are attempted.
-- First row reaches capacity; second row is rejected.
-- Entire multi-row INSERT is rolled back.

DELIMITER //

CREATE PROCEDURE usp_TestMultiRowAdmission()
BEGIN
    DECLARE v_failed INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET v_failed = 1;

    INSERT INTO admissions
    (patient_name, ward_id, status)
    VALUES
    ('Patient A', 1, 'Admitted'),
    ('Patient B', 1, 'Admitted');

    IF v_failed = 1 THEN
        SELECT
        'Admission batch rejected. Entire INSERT rolled back.'
        AS Result;
    ELSE
        SELECT
        'All admissions successful.'
        AS Result;
    END IF;
END //

DELIMITER ;

CALL usp_TestMultiRowAdmission();


-- TASK 4: TRIGGER LIMITS

-- Risk 1: Nested triggers
-- One trigger may execute operations that activate other triggers.

-- Risk 2: Recursive triggers
-- A trigger may indirectly cause itself to execute repeatedly.

-- Prevention:
-- Use conditional checks, avoid unnecessary updates to
-- triggering tables and keep trigger dependencies simple.

-- A CHECK constraint is better for simple row-level rules.
-- A stored procedure is better when admission requires
-- multiple validations, transactions and detailed error handling.

-- FINAL VERIFICATION

SELECT * FROM wards;

SELECT * FROM admissions;

SELECT * FROM admission_audit;
