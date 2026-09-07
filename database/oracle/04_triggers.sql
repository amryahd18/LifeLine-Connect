-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 4 - Production Database Triggers & Audit Logging
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- ============================================================================

-- 1. Create Audit Table for Dispatches
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

-- ============================================================================
-- 2. TRIGGER: TRG_DONOR_POST_DONATION
-- Automatically updates Donor's last donation date and computes next eligibility
-- date (+56 days interval for whole blood safety)
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
-- 3. TRIGGER: TRG_INVENTORY_AUTO_EXPIRE
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
-- 4. TRIGGER: TRG_AUDIT_DISPATCH
-- Immutable audit log for every blood unit dispatched to partner hospitals
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
