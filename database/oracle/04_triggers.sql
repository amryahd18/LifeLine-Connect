-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 4 - Production Database Triggers, Audit Ledgers & Views
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- Features: Row-level triggers, audit ledgers, validation guards, automated views
-- ============================================================================

-- ============================================================================
-- 1. AUDIT TABLES
-- ============================================================================

-- Audit table for hospital dispatches
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE AUDIT_DISPATCH_LOG CASCADE CONSTRAINTS';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

CREATE TABLE AUDIT_DISPATCH_LOG (
    log_id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dispatch_id         NUMBER NOT NULL,
    request_id          NUMBER NOT NULL,
    unit_id             NUMBER NOT NULL,
    dispatched_by       NUMBER,
    log_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    action_type         VARCHAR2(50) DEFAULT 'DISPATCH_FULFILLED' NOT NULL,
    notes               VARCHAR2(300)
)
/

-- Audit table for donor demographic and clinical updates
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE DONOR_AUDIT_HISTORY CASCADE CONSTRAINTS';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

CREATE TABLE DONOR_AUDIT_HISTORY (
    audit_id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    donor_id            NUMBER NOT NULL,
    field_changed       VARCHAR2(50) NOT NULL,
    old_value           VARCHAR2(200),
    new_value           VARCHAR2(200),
    changed_by          VARCHAR2(50) DEFAULT USER,
    changed_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
/

-- ============================================================================
-- 2. TRIGGER: TRG_DONOR_PRE_VALIDATE (Validation & Normalization Guard)
-- Runs BEFORE INSERT OR UPDATE ON DONORS
-- - Formats names to Title Case, emails to lowercase
-- - Validates that donor is at least 18 years of age
-- - Automatically sets initial next_eligible_date if NULL
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_DONOR_PRE_VALIDATE
BEFORE INSERT OR UPDATE ON DONORS
FOR EACH ROW
BEGIN
    :NEW.email := LOWER(TRIM(:NEW.email));
    :NEW.first_name := INITCAP(TRIM(:NEW.first_name));
    :NEW.last_name := INITCAP(TRIM(:NEW.last_name));
    
    -- Clinical rule: Minimum age 18 years
    IF MONTHS_BETWEEN(TRUNC(SYSDATE), :NEW.date_of_birth) / 12 < 18 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Clinical Safety Policy: Donor must be at least 18 years of age.');
    END IF;

    -- Set default initial eligibility date to today if not provided
    IF :NEW.next_eligible_date IS NULL THEN
        :NEW.next_eligible_date := TRUNC(SYSDATE);
    END IF;
END;
/

-- ============================================================================
-- 3. TRIGGER: TRG_DONOR_POST_DONATION (Cooldown Scheduling)
-- Automatically updates Donor's last donation date and computes next eligibility
-- date (+56 days cooldown for whole blood safety)
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_DONOR_POST_DONATION
AFTER INSERT ON DONATION_RECORDS
FOR EACH ROW
WHEN (NEW.screening_status = 'PASSED')
BEGIN
    UPDATE DONORS
    SET last_donation_date = :NEW.donation_date,
        next_eligible_date = :NEW.donation_date + 56,
        eligibility_status = 'TEMPORARILY_DEFERRED' -- Deferred until next_eligible_date passes
    WHERE donor_id = :NEW.donor_id;
END;
/

-- ============================================================================
-- 4. TRIGGER: TRG_INVENTORY_AUTO_EXPIRE (Automated Expiration Check)
-- Enforces inventory validity and auto-marks units as EXPIRED if past shelf life
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_INVENTORY_AUTO_EXPIRE
BEFORE INSERT OR UPDATE ON BLOOD_INVENTORY
FOR EACH ROW
BEGIN
    IF :NEW.expiration_date < TRUNC(SYSDATE) AND :NEW.status = 'AVAILABLE' THEN
        :NEW.status := 'EXPIRED';
    END IF;
END;
/

-- ============================================================================
-- 5. TRIGGER: TRG_PREVENT_EXPIRED_DISPATCH (Clinical Safety Guard)
-- Prevents physical dispatch of expired or non-existent blood units
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_PREVENT_EXPIRED_DISPATCH
BEFORE INSERT ON BLOOD_DISPATCHES
FOR EACH ROW
DECLARE
    v_exp DATE;
    v_status VARCHAR2(20);
BEGIN
    SELECT expiration_date, status INTO v_exp, v_status
    FROM BLOOD_INVENTORY
    WHERE unit_id = :NEW.unit_id;

    IF v_exp < TRUNC(SYSDATE) OR v_status = 'EXPIRED' THEN
        RAISE_APPLICATION_ERROR(-20002, 'Clinical Safety Violation: Cannot dispatch expired blood unit #' || :NEW.unit_id);
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Inventory Error: Blood unit #' || :NEW.unit_id || ' does not exist in inventory.');
END;
/

-- ============================================================================
-- 6. TRIGGER: TRG_AUDIT_DISPATCH (Audit Trail Logging)
-- Immutable audit log entry for every blood unit dispatched to partner hospitals
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_AUDIT_DISPATCH
AFTER INSERT ON BLOOD_DISPATCHES
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_DISPATCH_LOG (
        dispatch_id, request_id, unit_id, dispatched_by, log_timestamp, action_type, notes
    ) VALUES (
        :NEW.dispatch_id,
        :NEW.request_id,
        :NEW.unit_id,
        :NEW.dispatched_by,
        CURRENT_TIMESTAMP,
        'DISPATCH_FULFILLED',
        'Transporter: ' || :NEW.transporter_name || ' | Status: ' || :NEW.delivery_status
    );
END;
/

-- ============================================================================
-- 7. TRIGGER: TRG_DONOR_AUDIT_HISTORY (Audit Log on Updates)
-- Records changes to donor eligibility, contact phone, or weight
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_DONOR_AUDIT_HISTORY
AFTER UPDATE ON DONORS
FOR EACH ROW
BEGIN
    IF :OLD.eligibility_status != :NEW.eligibility_status THEN
        INSERT INTO DONOR_AUDIT_HISTORY (donor_id, field_changed, old_value, new_value)
        VALUES (:NEW.donor_id, 'ELIGIBILITY_STATUS', :OLD.eligibility_status, :NEW.eligibility_status);
    END IF;

    IF :OLD.weight_kg != :NEW.weight_kg THEN
        INSERT INTO DONOR_AUDIT_HISTORY (donor_id, field_changed, old_value, new_value)
        VALUES (:NEW.donor_id, 'WEIGHT_KG', TO_CHAR(:OLD.weight_kg), TO_CHAR(:NEW.weight_kg));
    END IF;

    IF :OLD.phone != :NEW.phone THEN
        INSERT INTO DONOR_AUDIT_HISTORY (donor_id, field_changed, old_value, new_value)
        VALUES (:NEW.donor_id, 'PHONE', :OLD.phone, :NEW.phone);
    END IF;
END;
/

-- ============================================================================
-- 8. TRIGGER: TRG_REQ_AUTO_STATUS (Requisition Lifecycle Automation)
-- Automatically advances blood request status based on fulfilled units
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_REQ_AUTO_STATUS
BEFORE UPDATE ON BLOOD_REQUESTS
FOR EACH ROW
BEGIN
    IF :NEW.units_fulfilled >= :NEW.units_requested AND :NEW.status NOT IN ('CANCELLED', 'REJECTED') THEN
        :NEW.status := 'DISPATCHED';
    ELSIF :NEW.units_fulfilled > 0 AND :NEW.units_fulfilled < :NEW.units_requested AND :NEW.status NOT IN ('CANCELLED', 'REJECTED') THEN
        :NEW.status := 'PARTIAL';
    END IF;
END;
/

-- ============================================================================
-- 9. PRODUCTION ORACLE VIEWS
-- ============================================================================

-- View 1: Real-time FEFO Available Inventory with days to expiry
CREATE OR REPLACE VIEW VW_AVAILABLE_FEFO_INVENTORY AS
SELECT unit_id, donation_id, blood_group, component_type, collection_date, expiration_date,
       ROUND(expiration_date - TRUNC(SYSDATE)) AS days_to_expiry,
       storage_location, status
FROM BLOOD_INVENTORY
WHERE status = 'AVAILABLE' AND expiration_date >= TRUNC(SYSDATE);

-- View 2: Critical Pending Hospital Orders
CREATE OR REPLACE VIEW VW_CRITICAL_HOSPITAL_ORDERS AS
SELECT r.request_id, h.hospital_name, h.category, h.city, h.phone,
       r.blood_group, r.component_type, r.units_requested, r.units_fulfilled,
       (r.units_requested - r.units_fulfilled) AS units_needed,
       r.urgency_level, r.required_by_date, r.status
FROM BLOOD_REQUESTS r
JOIN HOSPITALS h ON r.hospital_id = h.hospital_id
WHERE r.status IN ('PENDING', 'PARTIAL');

-- View 3: Camp Collection Progress Summary
CREATE OR REPLACE VIEW VW_CAMP_COLLECTION_SUMMARY AS
SELECT c.camp_id, c.camp_name, c.organizer_name, c.city, c.start_date, c.end_date,
       c.target_units, c.status,
       COUNT(DISTINCT d.donation_id) AS total_donations,
       NVL(SUM(d.units_donated), 0) AS total_units_collected,
       ROUND(NVL(SUM(d.units_donated), 0) / NULLIF(c.target_units, 0) * 100, 1) AS target_fulfillment_pct
FROM CAMPS c
LEFT JOIN DONATION_RECORDS d ON c.camp_id = d.camp_id AND d.screening_status = 'PASSED'
GROUP BY c.camp_id, c.camp_name, c.organizer_name, c.city, c.start_date, c.end_date, c.target_units, c.status;

COMMIT;
