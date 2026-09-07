# LifeLine Connect: Entity-Relationship Diagram (ERD) & Relational Schema Specification

## 1. Conceptual & Logical ER Diagram (Crow's Foot Notation)

```mermaid
erDiagram
    DONORS ||--o{ DONATION_RECORDS : "participates in"
    CAMPS ||--o{ DONATION_RECORDS : "hosts"
    CAMPS ||--o{ STAFF_ASSIGNMENTS : "schedules"
    STAFF ||--o{ STAFF_ASSIGNMENTS : "assigned to"
    STAFF ||--o{ BLOOD_DISPATCHES : "authorizes"
    DONATION_RECORDS ||--|| BLOOD_INVENTORY : "yields"
    HOSPITALS ||--o{ BLOOD_REQUESTS : "orders"
    BLOOD_REQUESTS ||--o{ BLOOD_DISPATCHES : "fulfilled by"
    BLOOD_INVENTORY ||--o| BLOOD_DISPATCHES : "allocated to"

    DONORS {
        NUMBER donor_id PK
        VARCHAR2 first_name
        VARCHAR2 last_name
        VARCHAR2 email UK
        VARCHAR2 phone
        DATE date_of_birth
        VARCHAR2 gender
        VARCHAR2 blood_group
        VARCHAR2 rh_factor
        NUMBER weight_kg
        NUMBER hemoglobin_level
        VARCHAR2 eligibility_status
        DATE last_donation_date
        DATE next_eligible_date
        VARCHAR2 address
        VARCHAR2 city
        TIMESTAMP created_at
    }

    CAMPS {
        NUMBER camp_id PK
        VARCHAR2 camp_name
        VARCHAR2 organizer_name
        VARCHAR2 venue_address
        VARCHAR2 city
        DATE start_date
        DATE end_date
        NUMBER target_units
        VARCHAR2 status
        TIMESTAMP created_at
    }

    STAFF {
        NUMBER staff_id PK
        VARCHAR2 first_name
        VARCHAR2 last_name
        VARCHAR2 role
        VARCHAR2 email UK
        VARCHAR2 phone
        VARCHAR2 license_number
        VARCHAR2 status
        TIMESTAMP created_at
    }

    STAFF_ASSIGNMENTS {
        NUMBER assignment_id PK
        NUMBER camp_id FK
        NUMBER staff_id FK
        VARCHAR2 role_assigned
        DATE shift_date
        NUMBER hours_worked
        VARCHAR2 status
    }

    DONATION_RECORDS {
        NUMBER donation_id PK
        NUMBER donor_id FK
        NUMBER camp_id FK
        DATE donation_date
        NUMBER units_donated
        NUMBER blood_pressure_sys
        NUMBER blood_pressure_dia
        NUMBER pulse_rate
        NUMBER hemoglobin_reading
        VARCHAR2 screening_status
        VARCHAR2 tested_status
        VARCHAR2 notes
        TIMESTAMP created_at
    }

    BLOOD_INVENTORY {
        NUMBER unit_id PK
        NUMBER donation_id FK,UK
        VARCHAR2 blood_group
        VARCHAR2 component_type
        DATE collection_date
        DATE expiration_date
        VARCHAR2 storage_location
        VARCHAR2 status
        TIMESTAMP created_at
    }

    HOSPITALS {
        NUMBER hospital_id PK
        VARCHAR2 hospital_name
        VARCHAR2 license_no UK
        VARCHAR2 category
        VARCHAR2 contact_person
        VARCHAR2 phone
        VARCHAR2 email
        VARCHAR2 address
        VARCHAR2 city
        TIMESTAMP created_at
    }

    BLOOD_REQUESTS {
        NUMBER request_id PK
        NUMBER hospital_id FK
        VARCHAR2 blood_group
        VARCHAR2 component_type
        NUMBER units_requested
        VARCHAR2 urgency_level
        DATE request_date
        DATE required_by_date
        NUMBER units_fulfilled
        VARCHAR2 status
        VARCHAR2 notes
        TIMESTAMP created_at
    }

    BLOOD_DISPATCHES {
        NUMBER dispatch_id PK
        NUMBER request_id FK
        NUMBER unit_id FK,UK
        TIMESTAMP dispatch_date
        NUMBER dispatched_by FK
        VARCHAR2 transporter_name
        VARCHAR2 delivery_status
        VARCHAR2 dispatch_notes
    }
```

---

## 2. Normalization Analysis (Third Normal Form - 3NF)

1. **First Normal Form (1NF)**:
   - All attribute values are atomic (single scalar values).
   - No repeating groups or multivalued arrays.
   - Unique primary keys defined for all entities using Oracle identity sequences (`GENERATED ALWAYS AS IDENTITY`).

2. **Second Normal Form (2NF)**:
   - Meets 1NF.
   - All non-key attributes are fully functionally dependent on the entire primary key. In all tables, composite keys have been replaced or augmented with surrogate primary keys (`assignment_id`, `donation_id`, etc.), completely eliminating partial key dependencies.

3. **Third Normal Form (3NF)**:
   - Meets 2NF.
   - No transitive dependencies exist ($X \to Y$ and $Y \to Z$). 
   - Hospital data is separated from request data; camp venue details are separated from donation events; screening vitals belong to specific donation transactions; blood component parameters and expiration dates are decoupled from donor registration.

---

## 3. Referential Integrity & Business Rules
- **Donor Eligibility**: Hemoglobin must be $\ge 8.0\text{ g/dL}$ (clinical screening requires $\ge 12.0$ for passed status), weight $\ge 45\text{ kg}$, with standard status lifecycle.
- **First-Expired, First-Out (FEFO)**: Blood units track precise component shelf lives (RBC: 42 days, Platelets: 5 days, Whole Blood: 35 days, Plasma: 365 days).
- **Hospital Requisitions**: Strict priority grading (`CRITICAL_EMERGENCY`, `URGENT`, `NORMAL`) with dispatch linkage.
- **Audit & Performance**: Comprehensive B-Tree indexing on foreign keys and frequently filtered query dimensions (`blood_group`, `status`, `expiration_date`).
