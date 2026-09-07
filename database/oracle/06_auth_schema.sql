-- ============================================================================
-- Project: LifeLine Connect (Blood Bank Network)
-- Component: User Authentication & Role Access Control Schema - Sri Lanka Edition
-- Database: Oracle Database 21c Express Edition (XEPDB1)
-- Schema: LIFELINE_USER
-- ============================================================================

BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE USERS CASCADE CONSTRAINTS PURGE';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

CREATE TABLE USERS (
    user_id         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 101) PRIMARY KEY,
    username        VARCHAR2(50) NOT NULL,
    email           VARCHAR2(100) NOT NULL,
    password_hash   VARCHAR2(255) NOT NULL,
    full_name       VARCHAR2(100) NOT NULL,
    role            VARCHAR2(20) DEFAULT 'DONOR' NOT NULL,
    donor_id        NUMBER,
    hospital_id     NUMBER,
    staff_id        NUMBER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- Constraints
    CONSTRAINT uq_user_username UNIQUE (username),
    CONSTRAINT uq_user_email UNIQUE (email),
    CONSTRAINT chk_user_role CHECK (role IN ('ADMIN', 'STAFF', 'HOSPITAL', 'DONOR')),
    CONSTRAINT fk_user_donor FOREIGN KEY (donor_id) REFERENCES DONORS(donor_id) ON DELETE SET NULL,
    CONSTRAINT fk_user_hosp FOREIGN KEY (hospital_id) REFERENCES HOSPITALS(hospital_id) ON DELETE SET NULL,
    CONSTRAINT fk_user_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id) ON DELETE SET NULL
);

CREATE INDEX idx_user_login ON USERS(username, email);
CREATE INDEX idx_user_role ON USERS(role);

-- Seed Default Sri Lankan Accounts for System Access & Demonstration
-- Passwords:
-- admin: AdminPass123#
-- dr_perera: StaffPass123#
-- kasun_fernando: DonorPass123#
-- nhsl_colombo: HospPass123#

INSERT INTO USERS (username, email, password_hash, full_name, role, donor_id, hospital_id, staff_id)
VALUES (
    'admin',
    'admin@lifeline.org',
    'scrypt:32768:8:1$m7nWNLKp8Zq7Tzkp$d095f0a517e207e7863e62e0521c05f5a512742c21ff2f634b3ac9e14b96b6c9e2359aa18c00aff32ee9bdc91dc282f72f1d2ba51951461163eebfbe9039341a',
    'System Administrator (NBTS Sri Lanka)',
    'ADMIN',
    NULL, NULL, NULL
);

INSERT INTO USERS (username, email, password_hash, full_name, role, donor_id, hospital_id, staff_id)
VALUES (
    'dr_perera',
    'k.perera@nbts.health.gov.lk',
    'scrypt:32768:8:1$aXQcvo1fc1bPeNhC$1a934847de1d46d99f11ec82e03ce4e78ec65363830984da147665cfabfbd0139797d7459260768f7ca591760ab6153d6795d606040fa00b95cce71633689cd4',
    'Dr. Kavinga Perera',
    'STAFF',
    NULL, NULL, 3001
);

INSERT INTO USERS (username, email, password_hash, full_name, role, donor_id, hospital_id, staff_id)
VALUES (
    'kasun_fernando',
    'kasun.fernando@email.lk',
    'scrypt:32768:8:1$aBEON7UFLw4ln1Ix$c289c2ef27cbd0d778becf76f3eec2f47e590d95d1e6a521767ae2e7cd1499411fda9beb79d81ecc6b922855e936aed3f5b80b71709a2a379455bad3bcfe79df',
    'Kasun Fernando',
    'DONOR',
    1001, NULL, NULL
);

INSERT INTO USERS (username, email, password_hash, full_name, role, donor_id, hospital_id, staff_id)
VALUES (
    'nhsl_colombo',
    'bloodbank@nhsl.health.gov.lk',
    'scrypt:32768:8:1$fq5jvWh2vgVJEWFz$29b127e769f6b1ebbd94c44dfe81d9304d64571b769a0cabfe75e702d36a1438855dbf564cce72b3212f0f072f87aa06d4c0d12f884978de5882d84404a7df1c',
    'National Hospital of Sri Lanka Blood Bank',
    'HOSPITAL',
    NULL, 7001, NULL
);

COMMIT;
