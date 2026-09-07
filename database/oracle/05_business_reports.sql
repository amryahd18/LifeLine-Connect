-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 4 - Exactly 5 Production PL/SQL Business Reports
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- ============================================================================

CREATE OR REPLACE PACKAGE PKG_LIFELINE_REPORTS AS

    -- Report 1: Total Blood Units Collected by Blood Group Across Different Camps
    PROCEDURE sp_report_camps_collections (
        o_cursor OUT SYS_REFCURSOR
    );
    FUNCTION fn_report_camps_collections 
    RETURN SYS_REFCURSOR;

    -- Report 2: Blood Inventory Levels and Identification of Expiring Units
    PROCEDURE sp_report_inventory_expiring (
        p_days_ahead IN NUMBER,
        o_cursor OUT SYS_REFCURSOR
    );
    FUNCTION fn_report_inventory_expiring (
        p_days_ahead IN NUMBER DEFAULT 7
    ) RETURN SYS_REFCURSOR;

    -- Report 3: Individual Donor Eligibility and Donation History Summaries
    PROCEDURE sp_report_donor_history (
        p_donor_id         IN NUMBER,
        o_summary_cursor   OUT SYS_REFCURSOR,
        o_history_cursor   OUT SYS_REFCURSOR
    );
    FUNCTION fn_report_donor_summary (
        p_donor_id IN NUMBER
    ) RETURN SYS_REFCURSOR;
    FUNCTION fn_report_donor_history (
        p_donor_id IN NUMBER
    ) RETURN SYS_REFCURSOR;

    -- Report 4: Hospital Blood Demand & Fulfillment Efficiency Report
    PROCEDURE sp_report_hospital_fulfillment (
        o_cursor OUT SYS_REFCURSOR
    );
    FUNCTION fn_report_hospital_fulfillment 
    RETURN SYS_REFCURSOR;

    -- Report 5: Staff & Volunteer Deployment and Operational Workload Report
    PROCEDURE sp_report_staff_workload (
        o_cursor OUT SYS_REFCURSOR
    );
    FUNCTION fn_report_staff_workload 
    RETURN SYS_REFCURSOR;

END PKG_LIFELINE_REPORTS;
/

CREATE OR REPLACE PACKAGE BODY PKG_LIFELINE_REPORTS AS

    -- ------------------------------------------------------------------------
    -- Report 1: Total Blood Units Collected by Blood Group Across Camps
    -- ------------------------------------------------------------------------
    FUNCTION fn_report_camps_collections RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                NVL(c.camp_name, 'Central Facility (Walk-in)') AS camp_name,
                NVL(c.city, 'Headquarters') AS venue_city,
                NVL(c.status, 'PERMANENT') AS camp_status,
                d.blood_group,
                COUNT(dr.donation_id) AS total_donations,
                SUM(dr.units_donated) AS total_units_collected,
                COUNT(DISTINCT dr.donor_id) AS distinct_donors,
                NVL(c.target_units, 0) AS camp_target_units
            FROM DONATION_RECORDS dr
            JOIN DONORS d ON dr.donor_id = d.donor_id
            LEFT JOIN CAMPS c ON dr.camp_id = c.camp_id
            WHERE dr.screening_status = 'PASSED'
            GROUP BY c.camp_name, c.city, c.status, d.blood_group, c.target_units
            ORDER BY camp_name, d.blood_group;
        RETURN v_cursor;
    END fn_report_camps_collections;

    PROCEDURE sp_report_camps_collections (
        o_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        o_cursor := fn_report_camps_collections();
    END sp_report_camps_collections;

    -- ------------------------------------------------------------------------
    -- Report 2: Inventory Levels and Expiring Units within p_days_ahead
    -- ------------------------------------------------------------------------
    FUNCTION fn_report_inventory_expiring (
        p_days_ahead IN NUMBER DEFAULT 7
    ) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
        v_window NUMBER := NVL(p_days_ahead, 7);
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                bi.unit_id,
                bi.blood_group,
                bi.component_type,
                bi.storage_location,
                bi.collection_date,
                bi.expiration_date,
                bi.status,
                ROUND(bi.expiration_date - TRUNC(SYSDATE)) AS days_remaining,
                CASE 
                    WHEN bi.expiration_date < TRUNC(SYSDATE) THEN 'EXPIRED'
                    WHEN bi.expiration_date <= TRUNC(SYSDATE) + v_window THEN 'CRITICAL_EXPIRING_SOON'
                    ELSE 'STABLE'
                END AS freshness_category
            FROM BLOOD_INVENTORY bi
            WHERE bi.status IN ('AVAILABLE', 'RESERVED', 'EXPIRED')
              AND bi.expiration_date <= (TRUNC(SYSDATE) + v_window)
            ORDER BY bi.expiration_date ASC, bi.blood_group;
        RETURN v_cursor;
    END fn_report_inventory_expiring;

    PROCEDURE sp_report_inventory_expiring (
        p_days_ahead IN NUMBER,
        o_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        o_cursor := fn_report_inventory_expiring(p_days_ahead);
    END sp_report_inventory_expiring;

    -- ------------------------------------------------------------------------
    -- Report 3: Individual Donor Eligibility & Donation History Summaries
    -- ------------------------------------------------------------------------
    FUNCTION fn_report_donor_summary (
        p_donor_id IN NUMBER
    ) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                d.donor_id,
                d.first_name || ' ' || d.last_name AS full_name,
                d.email,
                d.phone,
                d.blood_group,
                d.rh_factor,
                d.weight_kg,
                d.hemoglobin_level,
                d.eligibility_status,
                d.last_donation_date,
                d.next_eligible_date,
                CASE 
                    WHEN d.next_eligible_date IS NULL OR d.next_eligible_date <= TRUNC(SYSDATE) THEN 0
                    ELSE ROUND(d.next_eligible_date - TRUNC(SYSDATE))
                END AS days_until_eligible,
                COUNT(dr.donation_id) AS lifetime_donations,
                NVL(SUM(dr.units_donated), 0) AS lifetime_units_contributed
            FROM DONORS d
            LEFT JOIN DONATION_RECORDS dr ON d.donor_id = dr.donor_id AND dr.screening_status = 'PASSED'
            WHERE d.donor_id = p_donor_id
            GROUP BY d.donor_id, d.first_name, d.last_name, d.email, d.phone,
                     d.blood_group, d.rh_factor, d.weight_kg, d.hemoglobin_level,
                     d.eligibility_status, d.last_donation_date, d.next_eligible_date;
        RETURN v_cursor;
    END fn_report_donor_summary;

    FUNCTION fn_report_donor_history (
        p_donor_id IN NUMBER
    ) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                dr.donation_id,
                dr.donation_date,
                NVL(c.camp_name, 'Central Walk-in') AS venue_name,
                dr.units_donated,
                dr.blood_pressure_sys || '/' || dr.blood_pressure_dia AS blood_pressure,
                dr.pulse_rate,
                dr.hemoglobin_reading,
                dr.screening_status,
                dr.tested_status,
                dr.notes
            FROM DONATION_RECORDS dr
            LEFT JOIN CAMPS c ON dr.camp_id = c.camp_id
            WHERE dr.donor_id = p_donor_id
            ORDER BY dr.donation_date DESC;
        RETURN v_cursor;
    END fn_report_donor_history;

    PROCEDURE sp_report_donor_history (
        p_donor_id         IN NUMBER,
        o_summary_cursor   OUT SYS_REFCURSOR,
        o_history_cursor   OUT SYS_REFCURSOR
    ) IS
    BEGIN
        o_summary_cursor := fn_report_donor_summary(p_donor_id);
        o_history_cursor := fn_report_donor_history(p_donor_id);
    END sp_report_donor_history;

    -- ------------------------------------------------------------------------
    -- Report 4: Hospital Blood Demand & Fulfillment Efficiency Report
    -- ------------------------------------------------------------------------
    FUNCTION fn_report_hospital_fulfillment RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                h.hospital_id,
                h.hospital_name,
                h.category AS hospital_category,
                h.city,
                COUNT(br.request_id) AS total_requests,
                NVL(SUM(br.units_requested), 0) AS total_units_demanded,
                NVL(SUM(br.units_fulfilled), 0) AS total_units_fulfilled,
                NVL(SUM(br.units_requested - br.units_fulfilled), 0) AS pending_deficit,
                CASE 
                    WHEN SUM(br.units_requested) > 0 THEN 
                        ROUND((SUM(br.units_fulfilled) / SUM(br.units_requested)) * 100, 1)
                    ELSE 0 
                END AS fulfillment_rate_pct,
                COUNT(CASE WHEN br.urgency_level = 'CRITICAL_EMERGENCY' THEN 1 END) AS critical_emergency_requests,
                COUNT(CASE WHEN br.status = 'DISPATCHED' THEN 1 END) AS dispatched_requests_count
            FROM HOSPITALS h
            LEFT JOIN BLOOD_REQUESTS br ON h.hospital_id = br.hospital_id
            GROUP BY h.hospital_id, h.hospital_name, h.category, h.city
            ORDER BY total_units_demanded DESC, fulfillment_rate_pct ASC;
        RETURN v_cursor;
    END fn_report_hospital_fulfillment;

    PROCEDURE sp_report_hospital_fulfillment (
        o_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        o_cursor := fn_report_hospital_fulfillment();
    END sp_report_hospital_fulfillment;

    -- ------------------------------------------------------------------------
    -- Report 5: Staff & Volunteer Deployment and Operational Workload Report
    -- ------------------------------------------------------------------------
    FUNCTION fn_report_staff_workload RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT 
                s.staff_id,
                s.first_name || ' ' || s.last_name AS staff_name,
                s.role AS clinical_role,
                s.license_number,
                s.status AS employment_status,
                COUNT(sa.assignment_id) AS total_shifts_scheduled,
                COUNT(CASE WHEN sa.status = 'ATTENDED' THEN 1 END) AS shifts_attended,
                NVL(SUM(CASE WHEN sa.status = 'ATTENDED' THEN sa.hours_worked ELSE 0 END), 0) AS total_hours_worked,
                COUNT(DISTINCT sa.camp_id) AS camps_supported,
                CASE 
                    WHEN COUNT(sa.assignment_id) > 0 THEN
                        ROUND((COUNT(CASE WHEN sa.status = 'ATTENDED' THEN 1 END) / COUNT(sa.assignment_id)) * 100, 1)
                    ELSE 0 
                END AS shift_compliance_pct
            FROM STAFF s
            LEFT JOIN STAFF_ASSIGNMENTS sa ON s.staff_id = sa.staff_id
            GROUP BY s.staff_id, s.first_name, s.last_name, s.role, s.license_number, s.status
            ORDER BY total_hours_worked DESC, shifts_attended DESC;
        RETURN v_cursor;
    END fn_report_staff_workload;

    PROCEDURE sp_report_staff_workload (
        o_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        o_cursor := fn_report_staff_workload();
    END sp_report_staff_workload;

END PKG_LIFELINE_REPORTS;
/
