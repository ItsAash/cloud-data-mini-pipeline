-- =========================
-- PATIENTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INT CHECK (age >= 0),
    gender TEXT,
    blood_type TEXT
);

-- =========================
-- ADMISSIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    hospital TEXT,
    doctor TEXT,
    admission_type TEXT,
    date_of_admission DATE,
    discharge_date DATE,
    length_of_stay INT,
    room_number INT
);

-- =========================
-- MEDICAL RECORDS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS medical_records (
    record_id SERIAL PRIMARY KEY,
    admission_id INT REFERENCES admissions(admission_id),
    medical_condition TEXT,
    medication TEXT,
    test_results TEXT
);

-- =========================
-- BILLING TABLE
-- =========================
CREATE TABLE IF NOT EXISTS billing (
    billing_id SERIAL PRIMARY KEY,
    admission_id INT REFERENCES admissions(admission_id),
    insurance_provider TEXT,
    billing_amount NUMERIC(12,2)
);