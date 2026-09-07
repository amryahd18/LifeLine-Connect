-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 1 - Oracle Relational Database Schema (DDL)
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- Target: Fully Normalized (3NF) Production DDL Script
-- ============================================================================

-- Clean up existing objects if script is re-run
BEGIN
  FOR cur_rec IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || cur_rec.table_name || ' CASCADE CONSTRAINTS PURGE';
  END LOOP;
END;
/

-- ============================================================================
-- 1. TABLE: DONORS
-- Core donor registration, demographic vitals, and health eligibility
-- ============================================================================
CREATE TABLE DONORS (
    donor_id            NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1001) PRIMARY KEY,
    first_name          VARCHAR2(50) NOT NULL,
    last_name           VARCHAR2(50) NOT NULL,
    email               VARCHAR2(100) NOT NULL,
    phone               VARCHAR2(20) NOT NULL,
    date_of_birth       DATE NOT NULL,
    gender              VARCHAR2(10) NOT NULL,
    blood_group         VARCHAR2(5) NOT NULL,
    rh_factor           VARCHAR2(10) NOT NULL,
    weight_kg           NUMBER(5, 2) NOT NULL,
    hemoglobin_level    NUMBER(4, 2) NOT NULL,
    eligibility_status  VARCHAR2(30) DEFAULT 'ELIGIBLE' NOT NULL,
    last_donation_date  DATE,
    next_eligible_date  DATE,
    address             VARCHAR2(200),
    city                VARCHAR2(50) NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Constraints
    CONSTRAINT uq_donor_email UNIQUE (email),
    CONSTRAINT chk_donor_gender CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    CONSTRAINT chk_donor_blood_group CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    CONSTRAINT chk_donor_rh CHECK (rh_factor IN ('POSITIVE', 'NEGATIVE')),
    CONSTRAINT chk_donor_weight CHECK (weight_kg >= 45.0),
    CONSTRAINT chk_donor_hemoglobin CHECK (hemoglobin_level >= 8.0),
    CONSTRAINT chk_donor_eligibility CHECK (eligibility_status IN ('ELIGIBLE', 'TEMPORARILY_DEFERRED', 'PERMANENTLY_INELIGIBLE'))
);

-- ============================================================================
-- 2. TABLE: CAMPS
-- Blood donation camps catalogue, scheduled dates, and venue details
-- ============================================================================
CREATE TABLE CAMPS (
    camp_id             NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 2001) PRIMARY KEY,
    camp_name           VARCHAR2(100) NOT NULL,
    organizer_name      VARCHAR2(100) NOT NULL,
    venue_address       VARCHAR2(200) NOT NULL,
    city                VARCHAR2(50) NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE NOT NULL,
    target_units        NUMBER(5) DEFAULT 50 NOT NULL,
    status              VARCHAR2(20) DEFAULT 'UPCOMING' NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Constraints
    CONSTRAINT chk_camp_target CHECK (target_units > 0),
    CONSTRAINT chk_camp_dates CHECK (end_date >= start_date),
    CONSTRAINT chk_camp_status CHECK (status IN ('UPCOMING', 'ACTIVE', 'COMPLETED', 'CANCELLED'))
);

-- ============================================================================
-- 3. TABLE: STAFF
-- Clinical personnel, phlebotomists, and volunteers
-- ============================================================================
CREATE TABLE STAFF (
    staff_id            NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 3001) PRIMARY KEY,
    first_name          VARCHAR2(50) NOT NULL,
    last_name           VARCHAR2(50) NOT NULL,
    role                VARCHAR2(30) NOT NULL,
    email               VARCHAR2(100) NOT NULL,
    phone               VARCHAR2(20) NOT NULL,
    license_number      VARCHAR2(50),
    status              VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Constraints
    CONSTRAINT uq_staff_email UNIQUE (email),
    CONSTRAINT chk_staff_role CHECK (role IN ('DOCTOR', 'NURSE', 'PHLEBOTOMIST', 'COORDINATOR', 'VOLUNTEER')),
    CONSTRAINT chk_staff_status CHECK (status IN ('ACTIVE', 'ON_LEAVE', 'INACTIVE'))
);

-- ============================================================================
-- 4. TABLE: STAFF_ASSIGNMENTS
-- Assignment tracking for medical personnel and volunteers at camps
-- ============================================================================
CREATE TABLE STAFF_ASSIGNMENTS (
    assignment_id       NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 4001) PRIMARY KEY,
    camp_id             NUMBER NOT NULL,
    staff_id            NUMBER NOT NULL,
    role_assigned       VARCHAR2(30) NOT NULL,
    shift_date          DATE NOT NULL,
    hours_worked        NUMBER(4, 2) DEFAULT 8.0 NOT NULL,
    status              VARCHAR2(20) DEFAULT 'SCHEDULED' NOT NULL,
    -- Foreign Keys & Constraints
    CONSTRAINT fk_assign_camp FOREIGN KEY (camp_id) REFERENCES CAMPS(camp_id) ON DELETE CASCADE,
    CONSTRAINT fk_assign_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id) ON DELETE CASCADE,
    CONSTRAINT uq_staff_camp_shift UNIQUE (staff_id, camp_id, shift_date),
    CONSTRAINT chk_assign_hours CHECK (hours_worked >= 0),
    CONSTRAINT chk_assign_status CHECK (status IN ('SCHEDULED', 'ATTENDED', 'ABSENT'))
);

-- ============================================================================
-- 5. TABLE: DONATION_RECORDS
-- Physical pre-donation screening vitals, tests, and unit collection event
-- ============================================================================
CREATE TABLE DONATION_RECORDS (
    donation_id         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 5001) PRIMARY KEY,
    donor_id            NUMBER NOT NULL,
    camp_id             NUMBER, -- NULL if donated at central blood bank facility
    donation_date       DATE DEFAULT SYSDATE NOT NULL,
    units_donated       NUMBER(3, 1) DEFAULT 1.0 NOT NULL,
    blood_pressure_sys  NUMBER(3) NOT NULL,
    blood_pressure_dia  NUMBER(3) NOT NULL,
    pulse_rate          NUMBER(3) NOT NULL,
    hemoglobin_reading  NUMBER(4, 2) NOT NULL,
    screening_status    VARCHAR2(20) DEFAULT 'PASSED' NOT NULL,
    tested_status       VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    notes               VARCHAR2(300),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Foreign Keys & Constraints
    CONSTRAINT fk_donation_donor FOREIGN KEY (donor_id) REFERENCES DONORS(donor_id),
    CONSTRAINT fk_donation_camp FOREIGN KEY (camp_id) REFERENCES CAMPS(camp_id) ON DELETE SET NULL,
    CONSTRAINT chk_donation_units CHECK (units_donated > 0),
    CONSTRAINT chk_donation_bp_sys CHECK (blood_pressure_sys BETWEEN 80 AND 200),
    CONSTRAINT chk_donation_bp_dia CHECK (blood_pressure_dia BETWEEN 50 AND 130),
    CONSTRAINT chk_donation_pulse CHECK (pulse_rate BETWEEN 40 AND 160),
    CONSTRAINT chk_donation_hb CHECK (hemoglobin_reading >= 8.0),
    CONSTRAINT chk_donation_screening CHECK (screening_status IN ('PASSED', 'REJECTED')),
    CONSTRAINT chk_donation_tested CHECK (tested_status IN ('PENDING', 'PASSED', 'REJECTED'))
);

-- ============================================================================
-- 6. TABLE: BLOOD_INVENTORY
-- Separated blood components, storage temperature/location, and FEFO expiration
-- ============================================================================
CREATE TABLE BLOOD_INVENTORY (
    unit_id             NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 6001) PRIMARY KEY,
    donation_id         NUMBER NOT NULL,
    blood_group         VARCHAR2(5) NOT NULL,
    component_type      VARCHAR2(20) DEFAULT 'WHOLE_BLOOD' NOT NULL,
    collection_date     DATE NOT NULL,
    expiration_date     DATE NOT NULL,
    storage_location    VARCHAR2(50) NOT NULL,
    status              VARCHAR2(20) DEFAULT 'AVAILABLE' NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Foreign Keys & Constraints
    CONSTRAINT fk_inv_donation FOREIGN KEY (donation_id) REFERENCES DONATION_RECORDS(donation_id) ON DELETE CASCADE,
    CONSTRAINT uq_inv_donation UNIQUE (donation_id),
    CONSTRAINT chk_inv_blood_group CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    CONSTRAINT chk_inv_component CHECK (component_type IN ('WHOLE_BLOOD', 'RBC', 'PLATELETS', 'PLASMA')),
    CONSTRAINT chk_inv_expiry CHECK (expiration_date > collection_date),
    CONSTRAINT chk_inv_status CHECK (status IN ('AVAILABLE', 'RESERVED', 'TRANSFUSED', 'DISCARDED', 'EXPIRED'))
);

-- ============================================================================
-- 7. TABLE: HOSPITALS
-- Registered clinical facilities, emergency centers, and licensing
-- ============================================================================
CREATE TABLE HOSPITALS (
    hospital_id         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 7001) PRIMARY KEY,
    hospital_name       VARCHAR2(100) NOT NULL,
    license_no          VARCHAR2(50) NOT NULL,
    category            VARCHAR2(30) DEFAULT 'GOVERNMENT' NOT NULL,
    contact_person      VARCHAR2(100) NOT NULL,
    phone               VARCHAR2(20) NOT NULL,
    email               VARCHAR2(100) NOT NULL,
    address             VARCHAR2(200) NOT NULL,
    city                VARCHAR2(50) NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Constraints
    CONSTRAINT uq_hosp_license UNIQUE (license_no),
    CONSTRAINT chk_hosp_cat CHECK (category IN ('GOVERNMENT', 'PRIVATE', 'TRAUMA_CENTER', 'SPECIALTY_CLINIC'))
);

-- ============================================================================
-- 8. TABLE: BLOOD_REQUESTS
-- Hospital blood requisition orders, urgency levels, and fulfillment tracking
-- ============================================================================
CREATE TABLE BLOOD_REQUESTS (
    request_id          NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 8001) PRIMARY KEY,
    hospital_id         NUMBER NOT NULL,
    blood_group         VARCHAR2(5) NOT NULL,
    component_type      VARCHAR2(20) DEFAULT 'WHOLE_BLOOD' NOT NULL,
    units_requested     NUMBER(4) NOT NULL,
    urgency_level       VARCHAR2(25) DEFAULT 'NORMAL' NOT NULL,
    request_date        DATE DEFAULT SYSDATE NOT NULL,
    required_by_date    DATE NOT NULL,
    units_fulfilled     NUMBER(4) DEFAULT 0 NOT NULL,
    status              VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    notes               VARCHAR2(300),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Foreign Keys & Constraints
    CONSTRAINT fk_req_hospital FOREIGN KEY (hospital_id) REFERENCES HOSPITALS(hospital_id) ON DELETE CASCADE,
    CONSTRAINT chk_req_blood_group CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    CONSTRAINT chk_req_component CHECK (component_type IN ('WHOLE_BLOOD', 'RBC', 'PLATELETS', 'PLASMA')),
    CONSTRAINT chk_req_units_req CHECK (units_requested > 0),
    CONSTRAINT chk_req_units_ful CHECK (units_fulfilled >= 0),
    CONSTRAINT chk_req_urgency CHECK (urgency_level IN ('NORMAL', 'URGENT', 'CRITICAL_EMERGENCY')),
    CONSTRAINT chk_req_dates CHECK (required_by_date >= request_date),
    CONSTRAINT chk_req_status CHECK (status IN ('PENDING', 'PARTIAL', 'APPROVED', 'DISPATCHED', 'REJECTED', 'CANCELLED'))
);

-- ============================================================================
-- 9. TABLE: BLOOD_DISPATCHES
-- Traceable physical fulfillment and dispatch of inventory units to hospitals
-- ============================================================================
CREATE TABLE BLOOD_DISPATCHES (
    dispatch_id         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 9001) PRIMARY KEY,
    request_id          NUMBER NOT NULL,
    unit_id             NUMBER NOT NULL,
    dispatch_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    dispatched_by       NUMBER,
    transporter_name    VARCHAR2(100),
    delivery_status     VARCHAR2(20) DEFAULT 'IN_TRANSIT' NOT NULL,
    dispatch_notes      VARCHAR2(300),
    -- Foreign Keys & Constraints
    CONSTRAINT fk_disp_request FOREIGN KEY (request_id) REFERENCES BLOOD_REQUESTS(request_id) ON DELETE CASCADE,
    CONSTRAINT fk_disp_unit FOREIGN KEY (unit_id) REFERENCES BLOOD_INVENTORY(unit_id),
    CONSTRAINT fk_disp_staff FOREIGN KEY (dispatched_by) REFERENCES STAFF(staff_id) ON DELETE SET NULL,
    CONSTRAINT uq_disp_unit UNIQUE (unit_id),
    CONSTRAINT chk_disp_delivery CHECK (delivery_status IN ('IN_TRANSIT', 'DELIVERED', 'RETURNED'))
);

-- ============================================================================
-- INDEXES FOR HIGH-TRAFFIC & RELATIONAL JOIN PERFORMANCE
-- ============================================================================
CREATE INDEX idx_donor_bg ON DONORS(blood_group, eligibility_status);
CREATE INDEX idx_donor_city ON DONORS(city);
CREATE INDEX idx_camp_status_date ON CAMPS(status, start_date);
CREATE INDEX idx_assign_camp ON STAFF_ASSIGNMENTS(camp_id);
CREATE INDEX idx_assign_staff ON STAFF_ASSIGNMENTS(staff_id);
CREATE INDEX idx_donation_donor ON DONATION_RECORDS(donor_id);
CREATE INDEX idx_donation_camp ON DONATION_RECORDS(camp_id);
CREATE INDEX idx_inv_fefo ON BLOOD_INVENTORY(blood_group, status, expiration_date);
CREATE INDEX idx_inv_component ON BLOOD_INVENTORY(component_type, status);
CREATE INDEX idx_req_hosp ON BLOOD_REQUESTS(hospital_id);
CREATE INDEX idx_req_status_urg ON BLOOD_REQUESTS(status, urgency_level);
CREATE INDEX idx_disp_req ON BLOOD_DISPATCHES(request_id);

COMMIT;
