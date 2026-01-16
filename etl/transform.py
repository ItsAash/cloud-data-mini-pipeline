import pandas as pd

def transform_data(df):
    # --- Standardize column names ---
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # --- Clean names ---
    df["name"] = df["name"].str.title()
    df["doctor"] = df["doctor"].str.title()

    # --- Convert dates ---
    df["date_of_admission"] = pd.to_datetime(df["date_of_admission"])
    df["discharge_date"] = pd.to_datetime(df["discharge_date"])

    # --- Feature engineering ---
    df["length_of_stay"] = (
        df["discharge_date"] - df["date_of_admission"]
    ).dt.days

    # --- Remove bad data ---
    df = df.dropna(subset=["name", "date_of_admission", "discharge_date"])

    return df