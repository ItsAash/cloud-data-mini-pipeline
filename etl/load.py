import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    os.getenv("DB_HOST_URI")
)

def load_data(df: pd.DataFrame):

    # =============================
    # STEP 1 — LOAD PATIENTS
    # =============================
    print("Step 1: Loading patients...")

    patients_df = (
        df[["name", "age", "gender", "blood_type"]]
        .drop_duplicates()
    )

    patients_df.to_sql(
        "patients",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"✅ Loaded {len(patients_df)} patients")

    # =============================
    # STEP 2 — MAP patient_id
    # =============================
    patients_lookup = pd.read_sql(
        "SELECT patient_id, name FROM patients",
        engine
    )

    name_to_id = dict(
        zip(patients_lookup["name"], patients_lookup["patient_id"])
    )

    df["patient_id"] = df["name"].map(name_to_id)

    if df["patient_id"].isna().any():
        raise RuntimeError("❌ Patient ID mapping failed")

    # =============================
    # STEP 3 — LOAD ADMISSIONS
    # =============================
    print("Step 2: Loading admissions...")

    admissions_df = df[
        [
            "patient_id",
            "hospital",
            "doctor",
            "admission_type",
            "date_of_admission",
            "discharge_date",
            "length_of_stay",
            "room_number"
        ]
    ]

    admissions_df.to_sql(
        "admissions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"✅ Loaded {len(admissions_df)} admissions")

    # =============================
    # STEP 4 — MAP admission_id
    # =============================
    admission_map = pd.read_sql(
      """
      SELECT admission_id, patient_id, date_of_admission
      FROM admissions
      """,
      engine
    )

    # 🔑 FORCE DATETIME ALIGNMENT
    admission_map["date_of_admission"] = pd.to_datetime(
        admission_map["date_of_admission"]
    )

    df = df.merge(
        admission_map,
        on=["patient_id", "date_of_admission"],
        how="left"
    )

    if df["admission_id"].isna().any():
        raise RuntimeError("❌ Admission ID mapping failed")

    # =============================
    # STEP 5 — LOAD MEDICAL RECORDS
    # =============================
    print("Step 3: Loading medical records...")

    medical_df = df[
        [
            "admission_id",
            "medical_condition",
            "medication",
            "test_results"
        ]
    ]

    medical_df.to_sql(
        "medical_records",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    # =============================
    # STEP 6 — LOAD BILLING
    # =============================
    print("Step 4: Loading billing...")

    billing_df = df[
        [
            "admission_id",
            "insurance_provider",
            "billing_amount"
        ]
    ]

    billing_df.to_sql(
        "billing",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print("✅ ETL load completed successfully")