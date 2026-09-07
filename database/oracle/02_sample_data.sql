-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: Phase 1 - Realistic Sample Seed Data (DML) - Sri Lanka Edition
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- ============================================================================

-- Clean up existing data in reverse order of foreign key dependencies
DELETE FROM BLOOD_DISPATCHES;
DELETE FROM BLOOD_REQUESTS;
DELETE FROM HOSPITALS;
DELETE FROM BLOOD_INVENTORY;
DELETE FROM DONATION_RECORDS;
DELETE FROM STAFF_ASSIGNMENTS;
DELETE FROM STAFF;
DELETE FROM CAMPS;
DELETE FROM DONORS;
COMMIT;

-- ============================================================================
-- 1. SEED DONORS (12 Sri Lankan Donors covering all ABO/Rh groups and states)
-- ============================================================================
INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Kasun', 'Fernando', 'kasun.fernando@email.lk', '+94-77-123-4567', TO_DATE('1990-04-12', 'YYYY-MM-DD'), 'MALE', 'O+', 'POSITIVE', 78.5, 15.2, 'ELIGIBLE', TO_DATE('2026-05-10', 'YYYY-MM-DD'), TO_DATE('2026-07-05', 'YYYY-MM-DD'), '42 Havelock Road, Colombo 05', 'Colombo');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Dilini', 'Jayasinghe', 'dilini.j@email.lk', '+94-71-234-5678', TO_DATE('1995-08-23', 'YYYY-MM-DD'), 'FEMALE', 'O-', 'NEGATIVE', 62.0, 13.8, 'ELIGIBLE', TO_DATE('2026-06-01', 'YYYY-MM-DD'), TO_DATE('2026-07-27', 'YYYY-MM-DD'), '18 Peradeniya Road', 'Kandy');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Nuwan', 'Bandara', 'nuwan.b@email.lk', '+94-76-345-6789', TO_DATE('1988-11-30', 'YYYY-MM-DD'), 'MALE', 'A+', 'POSITIVE', 81.0, 16.0, 'ELIGIBLE', TO_DATE('2026-08-20', 'YYYY-MM-DD'), TO_DATE('2026-10-15', 'YYYY-MM-DD'), '88 Galle Road, Mount Lavinia', 'Colombo');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Kavindi', 'Silva', 'kavindi.silva@email.lk', '+94-70-456-7890', TO_DATE('1998-02-14', 'YYYY-MM-DD'), 'FEMALE', 'A-', 'NEGATIVE', 54.5, 12.8, 'ELIGIBLE', NULL, SYSDATE, '12 Bauddhaloka Mawatha, Colombo 04', 'Colombo');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Mohamed', 'Rifaz', 'm.rifaz@email.lk', '+94-77-567-8901', TO_DATE('1992-09-05', 'YYYY-MM-DD'), 'MALE', 'B+', 'POSITIVE', 73.0, 14.9, 'ELIGIBLE', TO_DATE('2026-08-25', 'YYYY-MM-DD'), TO_DATE('2026-10-20', 'YYYY-MM-DD'), '310 Kandy Road', 'Kurunegala');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Fatima', 'Farook', 'fatima.farook@email.lk', '+94-72-678-9012', TO_DATE('1994-06-19', 'YYYY-MM-DD'), 'FEMALE', 'B-', 'NEGATIVE', 58.0, 13.2, 'ELIGIBLE', TO_DATE('2026-04-15', 'YYYY-MM-DD'), TO_DATE('2026-06-10', 'YYYY-MM-DD'), '25 Hospital Road, Kalubowila', 'Dehiwala');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Thilina', 'Senaratne', 'thilina.s@email.lk', '+94-77-789-0123', TO_DATE('1985-03-11', 'YYYY-MM-DD'), 'MALE', 'AB+', 'POSITIVE', 88.0, 15.5, 'ELIGIBLE', TO_DATE('2026-08-10', 'YYYY-MM-DD'), TO_DATE('2026-10-05', 'YYYY-MM-DD'), '502 Marine Drive, Kollupitiya', 'Colombo');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Priya', 'Sivakumar', 'priya.s@email.lk', '+94-78-890-1234', TO_DATE('2001-12-01', 'YYYY-MM-DD'), 'FEMALE', 'AB-', 'NEGATIVE', 52.0, 12.5, 'ELIGIBLE', NULL, SYSDATE, '77 Temple Road', 'Jaffna');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Roshan', 'Mahanama', 'roshan.m@email.lk', '+94-71-901-2345', TO_DATE('1997-07-28', 'YYYY-MM-DD'), 'MALE', 'O+', 'POSITIVE', 70.0, 14.1, 'TEMPORARILY_DEFERRED', TO_DATE('2026-07-30', 'YYYY-MM-DD'), TO_DATE('2026-09-24', 'YYYY-MM-DD'), '21 Dharmapala Mawatha, Colombo 07', 'Colombo');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Chamari', 'Athapaththu', 'chamari.a@email.lk', '+94-77-012-3456', TO_DATE('1993-10-14', 'YYYY-MM-DD'), 'FEMALE', 'A+', 'POSITIVE', 64.0, 13.6, 'ELIGIBLE', TO_DATE('2026-05-18', 'YYYY-MM-DD'), TO_DATE('2026-07-13', 'YYYY-MM-DD'), '94 Negombo Road', 'Kurunegala');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Malinda', 'Warnapura', 'malinda.w@email.lk', '+94-75-123-7890', TO_DATE('1989-01-22', 'YYYY-MM-DD'), 'MALE', 'B+', 'POSITIVE', 85.0, 15.8, 'ELIGIBLE', TO_DATE('2026-08-01', 'YYYY-MM-DD'), TO_DATE('2026-09-26', 'YYYY-MM-DD'), '109 Matara Road', 'Galle');

INSERT INTO DONORS (first_name, last_name, email, phone, date_of_birth, gender, blood_group, rh_factor, weight_kg, hemoglobin_level, eligibility_status, last_donation_date, next_eligible_date, address, city)
VALUES ('Oshadi', 'Ranasinghe', 'oshadi.r@email.lk', '+94-76-234-8901', TO_DATE('2002-05-17', 'YYYY-MM-DD'), 'FEMALE', 'O-', 'NEGATIVE', 50.5, 11.2, 'TEMPORARILY_DEFERRED', NULL, SYSDATE + 30, '404 Kandy Road', 'Gampaha');

-- ============================================================================
-- 2. SEED CAMPS (5 Sri Lankan Donation Camps: Completed, Active, Upcoming)
-- ============================================================================
INSERT INTO CAMPS (camp_name, organizer_name, venue_address, city, start_date, end_date, target_units, status)
VALUES ('Viharamahadevi Park Mega Blood Drive', 'Rotary Club of Colombo West & NBTS', 'Open Air Theatre Grounds, Colombo 07', 'Colombo', TO_DATE('2026-08-15', 'YYYY-MM-DD'), TO_DATE('2026-08-16', 'YYYY-MM-DD'), 120, 'COMPLETED');

INSERT INTO CAMPS (camp_name, organizer_name, venue_address, city, start_date, end_date, target_units, status)
VALUES ('University of Moratuwa Blood Fair', 'Rotaract Club of Univ. of Moratuwa', 'University Gymnasium, Katubedda', 'Moratuwa', TO_DATE('2026-08-24', 'YYYY-MM-DD'), TO_DATE('2026-08-25', 'YYYY-MM-DD'), 100, 'COMPLETED');

INSERT INTO CAMPS (camp_name, organizer_name, venue_address, city, start_date, end_date, target_units, status)
VALUES ('Faculty of Medicine National Camp', 'Medical Students Union & NBTS', 'Physiology Quadrangle, Kynsey Rd, Colombo 08', 'Colombo', TO_DATE('2026-09-01', 'YYYY-MM-DD'), TO_DATE('2026-09-06', 'YYYY-MM-DD'), 180, 'ACTIVE');

INSERT INTO CAMPS (camp_name, organizer_name, venue_address, city, start_date, end_date, target_units, status)
VALUES ('Kandy City Centre Blood Donation Drive', 'Lions Club of Kandy & Kandy TH', 'KCC Level 3 Atrium, Dalada Veediya', 'Kandy', TO_DATE('2026-09-15', 'YYYY-MM-DD'), TO_DATE('2026-09-16', 'YYYY-MM-DD'), 90, 'UPCOMING');

INSERT INTO CAMPS (camp_name, organizer_name, venue_address, city, start_date, end_date, target_units, status)
VALUES ('Galle Fort Heritage Blood Drive', 'Southern Provincial Health Directorate', 'Galle Fort Cultural Hall, Light House Street', 'Galle', TO_DATE('2026-09-28', 'YYYY-MM-DD'), TO_DATE('2026-09-29', 'YYYY-MM-DD'), 110, 'UPCOMING');

-- ============================================================================
-- 3. SEED STAFF (8 Medical Professionals & Cold-Chain Logistics Officers)
-- ============================================================================
INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Dr. Kavinga', 'Perera', 'DOCTOR', 'k.perera@nbts.health.gov.lk', '+94-77-222-0201', 'SLMC-38421', 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Dr. Nirmala', 'Weerasinghe', 'DOCTOR', 'n.weerasinghe@nbts.health.gov.lk', '+94-71-333-0202', 'SLMC-27320', 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Tharindu', 'Jayawardena', 'PHLEBOTOMIST', 't.jayawardena@nbts.health.gov.lk', '+94-76-444-0203', 'MLT-44129', 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Asela', 'Wickramasinghe', 'PHLEBOTOMIST', 'a.wickrama@nbts.health.gov.lk', '+94-77-555-0204', 'MLT-77210', 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Dr. Fatima', 'Rizwan', 'DOCTOR', 'f.rizwan@nbts.health.gov.lk', '+94-72-666-0205', 'SLMC-99341', 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Nuwan', 'Pradeep', 'COORDINATOR', 'n.pradeep@nbts.health.gov.lk', '+94-78-777-0206', NULL, 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Harshana', 'Dias', 'VOLUNTEER', 'h.dias@nbts.health.gov.lk', '+94-75-888-0207', NULL, 'ACTIVE');

INSERT INTO STAFF (first_name, last_name, role, email, phone, license_number, status)
VALUES ('Sanduni', 'Senanayake', 'VOLUNTEER', 's.senanayake@nbts.health.gov.lk', '+94-70-999-0208', NULL, 'ACTIVE');

-- ============================================================================
-- 4. SEED STAFF ASSIGNMENTS (Shift allocations at Camps)
-- ============================================================================
-- Camp 2001 (Viharamahadevi Park - Completed)
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2001, 3001, 'LEAD_PHYSICIAN', TO_DATE('2026-08-15', 'YYYY-MM-DD'), 8.5, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2001, 3003, 'TRIAGE_NURSE', TO_DATE('2026-08-15', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2001, 3004, 'PHLEBOTOMIST', TO_DATE('2026-08-15', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2001, 3006, 'VENUE_COORDINATOR', TO_DATE('2026-08-15', 'YYYY-MM-DD'), 9.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2001, 3007, 'DONOR_RECEPTION', TO_DATE('2026-08-15', 'YYYY-MM-DD'), 6.5, 'ATTENDED');

-- Camp 2002 (University of Moratuwa - Completed)
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2002, 3002, 'LEAD_PHYSICIAN', TO_DATE('2026-08-24', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2002, 3005, 'PHLEBOTOMIST', TO_DATE('2026-08-24', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2002, 3008, 'REFRESHMENT_SUPERVISOR', TO_DATE('2026-08-24', 'YYYY-MM-DD'), 7.0, 'ATTENDED');

-- Camp 2003 (Faculty of Medicine - Active)
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2003, 3001, 'LEAD_PHYSICIAN', TO_DATE('2026-09-02', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2003, 3003, 'TRIAGE_NURSE', TO_DATE('2026-09-02', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2003, 3004, 'PHLEBOTOMIST', TO_DATE('2026-09-02', 'YYYY-MM-DD'), 8.0, 'ATTENDED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2003, 3006, 'VENUE_COORDINATOR', TO_DATE('2026-09-02', 'YYYY-MM-DD'), 8.5, 'ATTENDED');

-- Camp 2004 (Kandy City Centre - Scheduled)
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2004, 3002, 'LEAD_PHYSICIAN', TO_DATE('2026-09-15', 'YYYY-MM-DD'), 0.0, 'SCHEDULED');
INSERT INTO STAFF_ASSIGNMENTS (camp_id, staff_id, role_assigned, shift_date, hours_worked, status)
VALUES (2004, 3005, 'PHLEBOTOMIST', TO_DATE('2026-09-15', 'YYYY-MM-DD'), 0.0, 'SCHEDULED');

-- ============================================================================
-- 5. SEED DONATION RECORDS (14 Donations across Donors & Camps)
-- ============================================================================
-- Kasun Fernando (O+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1001, 2001, TO_DATE('2026-08-15', 'YYYY-MM-DD'), 1.0, 118, 76, 68, 15.2, 'PASSED', 'PASSED', 'Regular Sri Lankan donor, excellent vitals.');

-- Dilini Jayasinghe (O-)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1002, 2001, TO_DATE('2026-08-15', 'YYYY-MM-DD'), 1.0, 110, 72, 70, 13.8, 'PASSED', 'PASSED', 'Universal donor unit prioritized for NHSL trauma emergency.');

-- Nuwan Bandara (A+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1003, 2001, TO_DATE('2026-08-16', 'YYYY-MM-DD'), 1.0, 122, 80, 72, 16.0, 'PASSED', 'PASSED', 'Apheresis platelet candidate for dengue patients.');

-- Mohamed Rifaz (B+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1005, 2002, TO_DATE('2026-08-24', 'YYYY-MM-DD'), 1.0, 120, 78, 65, 14.9, 'PASSED', 'PASSED', 'Donated at University of Moratuwa blood fair.');

-- Fatima Farook (B-)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1006, 2002, TO_DATE('2026-08-25', 'YYYY-MM-DD'), 1.0, 115, 74, 72, 13.2, 'PASSED', 'PASSED', 'Rare B-Negative unit collected.');

-- Thilina Senaratne (AB+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1007, 2001, TO_DATE('2026-08-15', 'YYYY-MM-DD'), 1.0, 128, 82, 74, 15.5, 'PASSED', 'PASSED', 'AB+ Plasma separation scheduled for burn unit.');

-- Roshan Mahanama (O+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1009, 2001, TO_DATE('2026-08-15', 'YYYY-MM-DD'), 1.0, 124, 78, 70, 14.1, 'PASSED', 'PASSED', 'Standard whole blood donation.');

-- Chamari Athapaththu (A+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1010, 2002, TO_DATE('2026-08-24', 'YYYY-MM-DD'), 1.0, 116, 70, 68, 13.6, 'PASSED', 'PASSED', 'Clean collection at campus drive.');

-- Malinda Warnapura (B+)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1011, 2001, TO_DATE('2026-08-16', 'YYYY-MM-DD'), 1.0, 126, 80, 75, 15.8, 'PASSED', 'PASSED', 'Good post-donation recovery.');

-- Active Camp 2003 (Faculty of Medicine) Donations:
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1001, 2003, TO_DATE('2026-09-02', 'YYYY-MM-DD'), 1.0, 120, 78, 70, 15.0, 'PASSED', 'PASSED', 'Medicine faculty drive donation.');

INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1002, 2003, TO_DATE('2026-09-02', 'YYYY-MM-DD'), 1.0, 112, 74, 72, 13.5, 'PASSED', 'PASSED', 'Critical O-Negative collection.');

INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1003, 2003, TO_DATE('2026-09-03', 'YYYY-MM-DD'), 1.0, 124, 82, 76, 15.9, 'PASSED', 'PASSED', 'Collected in good condition.');

-- Center walk-in donation at Central Blood Bank Narahenpita (camp_id is NULL)
INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1005, NULL, TO_DATE('2026-09-03', 'YYYY-MM-DD'), 1.0, 118, 75, 66, 14.7, 'PASSED', 'PASSED', 'Direct walk-in donation at NBTS Narahenpita HQ.');

INSERT INTO DONATION_RECORDS (donor_id, camp_id, donation_date, units_donated, blood_pressure_sys, blood_pressure_dia, pulse_rate, hemoglobin_reading, screening_status, tested_status, notes)
VALUES (1006, NULL, TO_DATE('2026-09-04', 'YYYY-MM-DD'), 1.0, 114, 72, 70, 13.1, 'PASSED', 'PASSED', 'Central facility collection.');

-- ============================================================================
-- 6. SEED BLOOD INVENTORY (14 Units with FEFO Expirations & Components)
-- ============================================================================
-- Unit 6001: from donation 5001 (O+ Whole Blood, collected Aug 15 -> exp Sep 19)
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5001, 'O+', 'WHOLE_BLOOD', TO_DATE('2026-08-15', 'YYYY-MM-DD'), TO_DATE('2026-09-19', 'YYYY-MM-DD'), 'Cold-Unit-A / Bay-1', 'AVAILABLE');

-- Unit 6002: from donation 5002 (O- RBC, collected Aug 15 -> exp Sep 26) - Dispatched to NHSL
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5002, 'O-', 'RBC', TO_DATE('2026-08-15', 'YYYY-MM-DD'), TO_DATE('2026-09-26', 'YYYY-MM-DD'), 'Cold-Unit-A / Bay-2', 'TRANSFUSED');

-- Unit 6003: from donation 5003 (A+ Platelets, collected Aug 16 -> expired Aug 21) - Expired
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5003, 'A+', 'PLATELETS', TO_DATE('2026-08-16', 'YYYY-MM-DD'), TO_DATE('2026-08-21', 'YYYY-MM-DD'), 'Agitator-1 / Tray-3', 'EXPIRED');

-- Unit 6004: from donation 5004 (B+ RBC, collected Aug 24 -> exp Oct 05) - Dispatched to Kalubowila
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5004, 'B+', 'RBC', TO_DATE('2026-08-24', 'YYYY-MM-DD'), TO_DATE('2026-10-05', 'YYYY-MM-DD'), 'Cold-Unit-B / Bay-1', 'TRANSFUSED');

-- Unit 6005: from donation 5005 (B- Whole Blood, collected Aug 25 -> exp Sep 29) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5005, 'B-', 'WHOLE_BLOOD', TO_DATE('2026-08-25', 'YYYY-MM-DD'), TO_DATE('2026-09-29', 'YYYY-MM-DD'), 'Cold-Unit-B / Bay-2', 'AVAILABLE');

-- Unit 6006: from donation 5006 (AB+ Plasma, collected Aug 15 -> exp Aug 15 next year) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5006, 'AB+', 'PLASMA', TO_DATE('2026-08-15', 'YYYY-MM-DD'), TO_DATE('2027-08-15', 'YYYY-MM-DD'), 'DeepFreezer-C / Shelf-1', 'AVAILABLE');

-- Unit 6007: from donation 5007 (O+ RBC, collected Aug 15 -> exp Sep 26) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5007, 'O+', 'RBC', TO_DATE('2026-08-15', 'YYYY-MM-DD'), TO_DATE('2026-09-26', 'YYYY-MM-DD'), 'Cold-Unit-A / Bay-3', 'AVAILABLE');

-- Unit 6008: from donation 5008 (A+ Whole Blood, collected Aug 24 -> exp Sep 28) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5008, 'A+', 'WHOLE_BLOOD', TO_DATE('2026-08-24', 'YYYY-MM-DD'), TO_DATE('2026-09-28', 'YYYY-MM-DD'), 'Cold-Unit-A / Bay-4', 'AVAILABLE');

-- Unit 6009: from donation 5009 (B+ RBC, collected Aug 16 -> exp Sep 27) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5009, 'B+', 'RBC', TO_DATE('2026-08-16', 'YYYY-MM-DD'), TO_DATE('2026-09-27', 'YYYY-MM-DD'), 'Cold-Unit-B / Bay-3', 'AVAILABLE');

-- Unit 6010: from donation 5010 (O+ Platelets, collected Sep 02 -> exp Sep 07) - EXPIRING IN 3 DAYS!
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5010, 'O+', 'PLATELETS', TO_DATE('2026-09-02', 'YYYY-MM-DD'), TO_DATE('2026-09-07', 'YYYY-MM-DD'), 'Agitator-1 / Tray-1', 'AVAILABLE');

-- Unit 6011: from donation 5011 (O- RBC, collected Sep 02 -> exp Oct 14) - Reserved for Emergency
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5011, 'O-', 'RBC', TO_DATE('2026-09-02', 'YYYY-MM-DD'), TO_DATE('2026-10-14', 'YYYY-MM-DD'), 'Cold-Unit-A / Bay-5', 'RESERVED');

-- Unit 6012: from donation 5012 (A+ Platelets, collected Sep 03 -> exp Sep 08) - EXPIRING IN 4 DAYS!
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5012, 'A+', 'PLATELETS', TO_DATE('2026-09-03', 'YYYY-MM-DD'), TO_DATE('2026-09-08', 'YYYY-MM-DD'), 'Agitator-1 / Tray-2', 'AVAILABLE');

-- Unit 6013: from donation 5013 (B+ Whole Blood, collected Sep 03 -> exp Oct 08) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5013, 'B+', 'WHOLE_BLOOD', TO_DATE('2026-09-03', 'YYYY-MM-DD'), TO_DATE('2026-10-08', 'YYYY-MM-DD'), 'Cold-Unit-B / Bay-4', 'AVAILABLE');

-- Unit 6014: from donation 5014 (B- Plasma, collected Sep 04 -> exp Sep 04 next year) - Safe
INSERT INTO BLOOD_INVENTORY (donation_id, blood_group, component_type, collection_date, expiration_date, storage_location, status)
VALUES (5014, 'B-', 'PLASMA', TO_DATE('2026-09-04', 'YYYY-MM-DD'), TO_DATE('2027-09-04', 'YYYY-MM-DD'), 'DeepFreezer-C / Shelf-2', 'AVAILABLE');

-- ============================================================================
-- 7. SEED HOSPITALS (5 Major Sri Lankan Healthcare Facilities)
-- ============================================================================
INSERT INTO HOSPITALS (hospital_name, license_no, category, contact_person, phone, email, address, city)
VALUES ('National Hospital of Sri Lanka (NHSL)', 'HOSP-SL-COL01', 'TRAUMA_CENTER', 'Dr. Catherine Stone (Director Transfusion)', '+94-11-269-1111', 'bloodbank@nhsl.health.gov.lk', 'Regent Street, Colombo 10', 'Colombo');

INSERT INTO HOSPITALS (hospital_name, license_no, category, contact_person, phone, email, address, city)
VALUES ('Colombo South Teaching Hospital (Kalubowila)', 'HOSP-SL-COL02', 'GOVERNMENT', 'Dr. Mark Henderson (Chief Hematologist)', '+94-11-276-3037', 'transfusion@kalubowila.health.gov.lk', 'Hospital Road, Kalubowila', 'Dehiwala');

INSERT INTO HOSPITALS (hospital_name, license_no, category, contact_person, phone, email, address, city)
VALUES ('Lady Ridgeway Hospital for Children (LRH)', 'HOSP-SL-COL03', 'SPECIALTY_CLINIC', 'Dr. Kelly Adams (Pediatric Transfusion)', '+94-11-269-3711', 'bloodbank@lrh.health.gov.lk', 'Dr. Danister De Silva Mawatha, Colombo 08', 'Colombo');

INSERT INTO HOSPITALS (hospital_name, license_no, category, contact_person, phone, email, address, city)
VALUES ('Teaching Hospital Kandy', 'HOSP-SL-CP01', 'GOVERNMENT', 'Dr. Paul Harrison (Head of Transfusion)', '+94-81-222-2261', 'bloodbank@kandyhospital.gov.lk', 'William Gopallawa Mawatha', 'Kandy');

INSERT INTO HOSPITALS (hospital_name, license_no, category, contact_person, phone, email, address, city)
VALUES ('Teaching Hospital Karapitiya (Galle)', 'HOSP-SL-SP01', 'GOVERNMENT', 'Dr. Samantha Green (Emergency Director)', '+94-91-223-2250', 'orders@karapitiya.health.gov.lk', 'Hirimbura Cross Road', 'Galle');

-- ============================================================================
-- 8. SEED BLOOD REQUESTS (8 Requests across urgency levels)
-- ============================================================================
-- Request 8001: NHSL Colombo - Critical Emergency Trauma (Dispatched)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7001, 'O-', 'RBC', 1, 'CRITICAL_EMERGENCY', TO_DATE('2026-08-20', 'YYYY-MM-DD'), TO_DATE('2026-08-20', 'YYYY-MM-DD'), 1, 'DISPATCHED', 'Emergency trauma victim massive hemorrhage in ICU.');

-- Request 8002: Kalubowila Hospital - Scheduled Surgeries (Dispatched)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7002, 'B+', 'RBC', 1, 'NORMAL', TO_DATE('2026-08-28', 'YYYY-MM-DD'), TO_DATE('2026-08-30', 'YYYY-MM-DD'), 1, 'DISPATCHED', 'Cardiovascular bypass scheduled procedure.');

-- Request 8003: Lady Ridgeway Hospital - Pediatric Dengue Platelets (Pending)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7003, 'A+', 'PLATELETS', 2, 'URGENT', TO_DATE('2026-09-03', 'YYYY-MM-DD'), TO_DATE('2026-09-05', 'YYYY-MM-DD'), 0, 'PENDING', 'Dengue hemorrhagic fever pediatric patient thrombocytopenia.');

-- Request 8004: NHSL Burns Unit - Critical Resuscitation (Approved)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7001, 'AB+', 'PLASMA', 2, 'URGENT', TO_DATE('2026-09-04', 'YYYY-MM-DD'), TO_DATE('2026-09-06', 'YYYY-MM-DD'), 0, 'APPROVED', 'Extensive third-degree burn fluid resuscitation.');

-- Request 8005: Karapitiya Hospital Galle - Emergency Maternity Bleeding (Pending)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7005, 'O+', 'WHOLE_BLOOD', 3, 'CRITICAL_EMERGENCY', TO_DATE('2026-09-04', 'YYYY-MM-DD'), TO_DATE('2026-09-04', 'YYYY-MM-DD'), 0, 'PENDING', 'Postpartum acute hemorrhage emergency in Galle maternity ward.');

-- Request 8006: Teaching Hospital Kandy - Orthopedic Surgery (Pending)
INSERT INTO BLOOD_REQUESTS (hospital_id, blood_group, component_type, units_requested, urgency_level, request_date, required_by_date, units_fulfilled, status, notes)
VALUES (7004, 'B-', 'WHOLE_BLOOD', 1, 'NORMAL', TO_DATE('2026-09-04', 'YYYY-MM-DD'), TO_DATE('2026-09-07', 'YYYY-MM-DD'), 0, 'PENDING', 'Elective orthopedic joint replacement prep.');

-- ============================================================================
-- 9. SEED BLOOD DISPATCHES (Traceable dispatches with Sri Lankan Couriers)
-- ============================================================================
-- Dispatch 9001: Fulfilling Request 8001 with Unit 6002 (O- RBC)
INSERT INTO BLOOD_DISPATCHES (request_id, unit_id, dispatch_date, dispatched_by, transporter_name, delivery_status, dispatch_notes)
VALUES (8001, 6002, TO_TIMESTAMP('2026-08-20 14:30:00', 'YYYY-MM-DD HH24:MI:SS'), 3006, '1990 Suwa Seriya Emergency Transporter (Van #WP-CAB-1990)', 'DELIVERED', 'Delivered within 25 minutes to NHSL Trauma Bay 4.');

-- Dispatch 9002: Fulfilling Request 8002 with Unit 6004 (B+ RBC)
INSERT INTO BLOOD_DISPATCHES (request_id, unit_id, dispatch_date, dispatched_by, transporter_name, delivery_status, dispatch_notes)
VALUES (8002, 6004, TO_TIMESTAMP('2026-08-29 09:15:00', 'YYYY-MM-DD HH24:MI:SS'), 3006, 'NBTS Cold-Chain Mobile Courier (WP-CAA-4491)', 'DELIVERED', 'Received and cold-stored by Kalubowila Blood Bank Lab.');

COMMIT;
