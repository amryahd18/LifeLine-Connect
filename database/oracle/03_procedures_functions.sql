-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 4 - PL/SQL Procedures, Functions & Exception Handling
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- ============================================================================

-- Create Package Specification for Core Business Operations
CREATE OR REPLACE PACKAGE PKG_LIFELINE_CORE AS
    -- Custom Exceptions
    EX_DONOR_INELIGIBLE     EXCEPTION;
    EX_INSUFFICIENT_STOCK   EXCEPTION;
    EX_CAMP_NOT_FOUND       EXCEPTION;
    EX_INVALID_VITALS       EXCEPTION;

    PRAGMA EXCEPTION_INIT(EX_DONOR_INELIGIBLE, -20001);
    PRAGMA EXCEPTION_INIT(EX_INSUFFICIENT_STOCK, -20002);
    PRAGMA EXCEPTION_INIT(EX_CAMP_NOT_FOUND, -20003);
    PRAGMA EXCEPTION_INIT(EX_INVALID_VITALS, -20004);

    -- 1. Function: Check Donor Eligibility
    FUNCTION fn_check_donor_eligibility(
        p_donor_id IN NUMBER
    ) RETURN VARCHAR2;

    -- 2. Procedure: Register a New Donor with Validation
    PROCEDURE sp_register_donor(
        p_first_name        IN VARCHAR2,
        p_last_name         IN VARCHAR2,
        p_email             IN VARCHAR2,
        p_phone             IN VARCHAR2,
        p_dob               IN DATE,
        p_gender            IN VARCHAR2,
        p_blood_group       IN VARCHAR2,
        p_rh_factor         IN VARCHAR2,
        p_weight_kg         IN NUMBER,
        p_hemoglobin        IN NUMBER,
        p_address           IN VARCHAR2,
        p_city              IN VARCHAR2,
        o_donor_id          OUT NUMBER,
        o_status_message    OUT VARCHAR2
    );

    -- 3. Procedure: Record Pre-Screening & Donation Event with Auto-Inventory Creation
    PROCEDURE sp_record_donation(
        p_donor_id          IN NUMBER,
        p_camp_id           IN NUMBER,
        p_bp_sys            IN NUMBER,
        p_bp_dia            IN NUMBER,
        p_pulse             IN NUMBER,
        p_hemoglobin        IN NUMBER,
        p_component_type    IN VARCHAR2,
        p_storage_location  IN VARCHAR2,
        p_notes             IN VARCHAR2,
        o_donation_id       OUT NUMBER,
        o_unit_id           OUT NUMBER,
        o_message           OUT VARCHAR2
    );

    -- 4. Procedure: Fulfill Hospital Request using FEFO (First-Expired, First-Out)
    PROCEDURE sp_fulfill_hospital_request(
        p_request_id        IN NUMBER,
        p_staff_id          IN NUMBER,
        p_transporter       IN VARCHAR2,
        o_dispatched_units  OUT NUMBER,
        o_status            OUT VARCHAR2,
        o_message           OUT VARCHAR2
    );

    -- 5. Procedure: Assign Staff/Volunteer to Camp Shift
    PROCEDURE sp_assign_staff_to_camp(
        p_camp_id           IN NUMBER,
        p_staff_id          IN NUMBER,
        p_role_assigned     IN VARCHAR2,
        p_shift_date        IN DATE,
        p_hours             IN NUMBER,
        o_assignment_id     OUT NUMBER,
        o_message           OUT VARCHAR2
    );
END PKG_LIFELINE_CORE;
/

-- Package Body
CREATE OR REPLACE PACKAGE BODY PKG_LIFELINE_CORE AS

    -- ------------------------------------------------------------------------
    -- 1. Function: Check Donor Eligibility
    -- ------------------------------------------------------------------------
    FUNCTION fn_check_donor_eligibility(
        p_donor_id IN NUMBER
    ) RETURN VARCHAR2 IS
        v_status            VARCHAR2(30);
        v_last_donation     DATE;
        v_next_eligible     DATE;
        v_weight            NUMBER;
        v_hb                NUMBER;
        v_days_since        NUMBER;
        v_age_years         NUMBER;
        v_dob               DATE;
    BEGIN
        SELECT eligibility_status, last_donation_date, next_eligible_date, weight_kg, hemoglobin_level, date_of_birth
        INTO v_status, v_last_donation, v_next_eligible, v_weight, v_hb, v_dob
        FROM DONORS
        WHERE donor_id = p_donor_id;

        -- Check age >= 18
        v_age_years := TRUNC(MONTHS_BETWEEN(SYSDATE, v_dob) / 12);
        IF v_age_years < 18 THEN
            RETURN 'INELIGIBLE: Donor age (' || v_age_years || ') is below 18 years.';
        END IF;

        -- Check permanent deferral
        IF v_status = 'PERMANENTLY_INELIGIBLE' THEN
            RETURN 'INELIGIBLE: Permanent medical deferral record.';
        END IF;

        -- Check weight >= 45 kg
        IF v_weight < 45.0 THEN
            RETURN 'INELIGIBLE: Donor weight (' || v_weight || 'kg) is below required 45kg.';
        END IF;

        -- Check hemoglobin >= 12.5 g/dL
        IF v_hb < 12.5 THEN
            RETURN 'TEMPORARILY_DEFERRED: Low hemoglobin level (' || v_hb || ' g/dL). Minimum is 12.5.';
        END IF;

        -- Check interval >= 56 days (8 weeks)
        IF v_last_donation IS NOT NULL THEN
            v_days_since := TRUNC(SYSDATE - v_last_donation);
            IF v_days_since < 56 THEN
                RETURN 'TEMPORARILY_DEFERRED: Only ' || v_days_since || ' days since last donation. Next eligible: ' || TO_CHAR(v_next_eligible, 'YYYY-MM-DD');
            END IF;
        END IF;

        RETURN 'ELIGIBLE';
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 'NOT_FOUND: Donor ID does not exist.';
        WHEN OTHERS THEN
            RETURN 'ERROR: ' || SQLERRM;
    END fn_check_donor_eligibility;

    -- ------------------------------------------------------------------------
    -- 2. Procedure: Register a New Donor
    -- ------------------------------------------------------------------------
    PROCEDURE sp_register_donor(
        p_first_name        IN VARCHAR2,
        p_last_name         IN VARCHAR2,
        p_email             IN VARCHAR2,
        p_phone             IN VARCHAR2,
        p_dob               IN DATE,
        p_gender            IN VARCHAR2,
        p_blood_group       IN VARCHAR2,
        p_rh_factor         IN VARCHAR2,
        p_weight_kg         IN NUMBER,
        p_hemoglobin        IN NUMBER,
        p_address           IN VARCHAR2,
        p_city              IN VARCHAR2,
        o_donor_id          OUT NUMBER,
        o_status_message    OUT VARCHAR2
    ) IS
        v_initial_status    VARCHAR2(30) := 'ELIGIBLE';
        v_age               NUMBER;
    BEGIN
        -- Age check
        v_age := TRUNC(MONTHS_BETWEEN(SYSDATE, p_dob) / 12);
        IF v_age < 18 THEN
            RAISE_APPLICATION_ERROR(-20004, 'Donor must be at least 18 years old. Calculated age: ' || v_age);
        END IF;

        IF p_weight_kg < 45.0 THEN
            RAISE_APPLICATION_ERROR(-20004, 'Donor weight must be at least 45 kg.');
        END IF;

        IF p_hemoglobin < 12.5 THEN
            v_initial_status := 'TEMPORARILY_DEFERRED';
        END IF;

        INSERT INTO DONORS (
            first_name, last_name, email, phone, date_of_birth,
            gender, blood_group, rh_factor, weight_kg, hemoglobin_level,
            eligibility_status, last_donation_date, next_eligible_date,
            address, city
        ) VALUES (
            p_first_name, p_last_name, p_email, p_phone, p_dob,
            p_gender, p_blood_group, p_rh_factor, p_weight_kg, p_hemoglobin,
            v_initial_status, NULL, SYSDATE,
            p_address, p_city
        ) RETURNING donor_id INTO o_donor_id;

        o_status_message := 'Donor successfully registered with ID: ' || o_donor_id || ' (Status: ' || v_initial_status || ')';
    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            o_donor_id := NULL;
            o_status_message := 'Registration failed: Email address already registered.';
        WHEN OTHERS THEN
            o_donor_id := NULL;
            o_status_message := 'Registration failed: ' || SQLERRM;
    END sp_register_donor;

    -- ------------------------------------------------------------------------
    -- 3. Procedure: Record Pre-Screening & Donation with Auto-Inventory Creation
    -- ------------------------------------------------------------------------
    PROCEDURE sp_record_donation(
        p_donor_id          IN NUMBER,
        p_camp_id           IN NUMBER,
        p_bp_sys            IN NUMBER,
        p_bp_dia            IN NUMBER,
        p_pulse             IN NUMBER,
        p_hemoglobin        IN NUMBER,
        p_component_type    IN VARCHAR2,
        p_storage_location  IN VARCHAR2,
        p_notes             IN VARCHAR2,
        o_donation_id       OUT NUMBER,
        o_unit_id           OUT NUMBER,
        o_message           OUT VARCHAR2
    ) IS
        v_eligibility       VARCHAR2(200);
        v_donor_bg          VARCHAR2(5);
        v_screen_status     VARCHAR2(20) := 'PASSED';
        v_shelf_life_days   NUMBER := 35;
        v_exp_date          DATE;
    BEGIN
        -- 1. Check donor eligibility
        v_eligibility := fn_check_donor_eligibility(p_donor_id);
        IF v_eligibility != 'ELIGIBLE' THEN
            RAISE_APPLICATION_ERROR(-20001, 'Donation Rejected: ' || v_eligibility);
        END IF;

        -- 2. Clinical screening vitals validation
        IF p_bp_sys > 180 OR p_bp_sys < 90 OR p_bp_dia > 100 OR p_bp_dia < 50 OR p_pulse < 50 OR p_pulse > 110 OR p_hemoglobin < 12.5 THEN
            v_screen_status := 'REJECTED';
            RAISE_APPLICATION_ERROR(-20004, 'Clinical screening failed: vitals out of safe donation range.');
        END IF;

        -- 3. Get Donor Blood Group
        SELECT blood_group INTO v_donor_bg FROM DONORS WHERE donor_id = p_donor_id;

        -- 4. Calculate component shelf life
        -- Whole blood = 35 days, RBC = 42 days, Platelets = 5 days, Plasma = 365 days
        CASE p_component_type
            WHEN 'RBC' THEN v_shelf_life_days := 42;
            WHEN 'PLATELETS' THEN v_shelf_life_days := 5;
            WHEN 'PLASMA' THEN v_shelf_life_days := 365;
            ELSE v_shelf_life_days := 35;
        END CASE;
        v_exp_date := TRUNC(SYSDATE) + v_shelf_life_days;

        -- 5. Insert Donation Record
        INSERT INTO DONATION_RECORDS (
            donor_id, camp_id, donation_date, units_donated,
            blood_pressure_sys, blood_pressure_dia, pulse_rate,
            hemoglobin_reading, screening_status, tested_status, notes
        ) VALUES (
            p_donor_id, p_camp_id, TRUNC(SYSDATE), 1.0,
            p_bp_sys, p_bp_dia, p_pulse,
            p_hemoglobin, v_screen_status, 'PASSED', p_notes
        ) RETURNING donation_id INTO o_donation_id;

        -- 6. Insert Blood Inventory Unit
        INSERT INTO BLOOD_INVENTORY (
            donation_id, blood_group, component_type,
            collection_date, expiration_date, storage_location, status
        ) VALUES (
            o_donation_id, v_donor_bg, p_component_type,
            TRUNC(SYSDATE), v_exp_date, p_storage_location, 'AVAILABLE'
        ) RETURNING unit_id INTO o_unit_id;

        -- Note: Trigger trg_donor_post_donation will update last_donation_date and next_eligible_date
        o_message := 'Donation ' || o_donation_id || ' accepted. Inventory unit ' || o_unit_id || ' stored at ' || p_storage_location || ' (Expires: ' || TO_CHAR(v_exp_date, 'YYYY-MM-DD') || ')';
    EXCEPTION
        WHEN OTHERS THEN
            o_donation_id := NULL;
            o_unit_id := NULL;
            o_message := 'Donation processing error: ' || SQLERRM;
            RAISE;
    END sp_record_donation;

    -- ------------------------------------------------------------------------
    -- 4. Procedure: Fulfill Hospital Request using FEFO
    -- ------------------------------------------------------------------------
    PROCEDURE sp_fulfill_hospital_request(
        p_request_id        IN NUMBER,
        p_staff_id          IN NUMBER,
        p_transporter       IN VARCHAR2,
        o_dispatched_units  OUT NUMBER,
        o_status            OUT VARCHAR2,
        o_message           OUT VARCHAR2
    ) IS
        v_req_bg            VARCHAR2(5);
        v_req_comp          VARCHAR2(20);
        v_req_units         NUMBER;
        v_units_fulfilled   NUMBER;
        v_remaining         NUMBER;
        v_count_allocated   NUMBER := 0;

        -- Cursor selecting units ordered by FEFO (First-Expired, First-Out)
        CURSOR c_fefo_units(cp_bg VARCHAR2, cp_comp VARCHAR2) IS
            SELECT unit_id, expiration_date
            FROM BLOOD_INVENTORY
            WHERE blood_group = cp_bg
              AND component_type = cp_comp
              AND status = 'AVAILABLE'
              AND expiration_date >= TRUNC(SYSDATE)
            ORDER BY expiration_date ASC
            FOR UPDATE;
    BEGIN
        SELECT blood_group, component_type, units_requested, units_fulfilled
        INTO v_req_bg, v_req_comp, v_req_units, v_units_fulfilled
        FROM BLOOD_REQUESTS
        WHERE request_id = p_request_id;

        v_remaining := v_req_units - v_units_fulfilled;
        IF v_remaining <= 0 THEN
            o_dispatched_units := 0;
            o_status := 'COMPLETED';
            o_message := 'Request already fully fulfilled.';
            RETURN;
        END IF;

        -- Loop through FEFO candidate inventory units
        FOR r_unit IN c_fefo_units(v_req_bg, v_req_comp) LOOP
            EXIT WHEN v_count_allocated >= v_remaining;

            -- 1. Create dispatch log
            INSERT INTO BLOOD_DISPATCHES (
                request_id, unit_id, dispatch_date,
                dispatched_by, transporter_name, delivery_status, dispatch_notes
            ) VALUES (
                p_request_id, r_unit.unit_id, SYSTIMESTAMP,
                p_staff_id, p_transporter, 'IN_TRANSIT', 'FEFO automated fulfillment.'
            );

            -- 2. Mark unit status as TRANSFUSED / DISPATCHED
            UPDATE BLOOD_INVENTORY
            SET status = 'TRANSFUSED'
            WHERE unit_id = r_unit.unit_id;

            v_count_allocated := v_count_allocated + 1;
        END LOOP;

        IF v_count_allocated = 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'Insufficient available inventory for blood group ' || v_req_bg || ' (' || v_req_comp || ').');
        END IF;

        -- 3. Update Request status
        UPDATE BLOOD_REQUESTS
        SET units_fulfilled = units_fulfilled + v_count_allocated,
            status = CASE WHEN (units_fulfilled + v_count_allocated) >= units_requested THEN 'DISPATCHED' ELSE 'PARTIAL' END
        WHERE request_id = p_request_id;

        SELECT status INTO o_status FROM BLOOD_REQUESTS WHERE request_id = p_request_id;
        o_dispatched_units := v_count_allocated;
        o_message := 'Successfully dispatched ' || v_count_allocated || ' unit(s) for Request #' || p_request_id || '. Status: ' || o_status;
    EXCEPTION
        WHEN OTHERS THEN
            o_dispatched_units := 0;
            o_status := 'ERROR';
            o_message := 'Fulfillment error: ' || SQLERRM;
            RAISE;
    END sp_fulfill_hospital_request;

    -- ------------------------------------------------------------------------
    -- 5. Procedure: Assign Staff to Camp Shift
    -- ------------------------------------------------------------------------
    PROCEDURE sp_assign_staff_to_camp(
        p_camp_id           IN NUMBER,
        p_staff_id          IN NUMBER,
        p_role_assigned     IN VARCHAR2,
        p_shift_date        IN DATE,
        p_hours             IN NUMBER,
        o_assignment_id     OUT NUMBER,
        o_message           OUT VARCHAR2
    ) IS
        v_staff_status      VARCHAR2(20);
        v_camp_status       VARCHAR2(20);
        v_conflict_count    NUMBER;
    BEGIN
        SELECT status INTO v_staff_status FROM STAFF WHERE staff_id = p_staff_id;
        IF v_staff_status != 'ACTIVE' THEN
            RAISE_APPLICATION_ERROR(-20001, 'Staff member is not active (Status: ' || v_staff_status || ').');
        END IF;

        SELECT status INTO v_camp_status FROM CAMPS WHERE camp_id = p_camp_id;
        IF v_camp_status = 'CANCELLED' THEN
            RAISE_APPLICATION_ERROR(-20003, 'Cannot assign staff to a cancelled camp.');
        END IF;

        -- Check duplicate shift on same date
        SELECT COUNT(*) INTO v_conflict_count
        FROM STAFF_ASSIGNMENTS
        WHERE staff_id = p_staff_id AND shift_date = p_shift_date;

        IF v_conflict_count > 0 THEN
            RAISE_APPLICATION_ERROR(-20004, 'Staff member already has an assigned shift on ' || TO_CHAR(p_shift_date, 'YYYY-MM-DD'));
        END IF;

        INSERT INTO STAFF_ASSIGNMENTS (
            camp_id, staff_id, role_assigned, shift_date, hours_worked, status
        ) VALUES (
            p_camp_id, p_staff_id, p_role_assigned, p_shift_date, p_hours, 'SCHEDULED'
        ) RETURNING assignment_id INTO o_assignment_id;

        o_message := 'Staff assigned successfully with Assignment ID: ' || o_assignment_id;
    EXCEPTION
        WHEN OTHERS THEN
            o_assignment_id := NULL;
            o_message := 'Assignment failed: ' || SQLERRM;
            RAISE;
    END sp_assign_staff_to_camp;

END PKG_LIFELINE_CORE;
/
