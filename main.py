import logging

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from db.init_db import init_db

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def main():
    try:
        logging.info("Step 1: Initializing database schema...")
        init_db()
        logging.info("✅ Database schema initialized successfully.")

        logging.info("Step 2: Extracting raw data from CSV...")
        df = extract_data("data/healthcare-raw.csv")
        logging.info(f"✅ Data extraction completed. {len(df)} rows loaded.")

        logging.info("Step 3: Transforming data...")
        df_clean = transform_data(df)
        logging.info(f"✅ Data transformation completed. {len(df_clean)} clean rows ready.")

        logging.info("Step 4: Loading data into the database...")
        load_data(df_clean)
        logging.info("✅ Data loading completed successfully.")

        logging.info("🎉 ETL pipeline executed successfully!")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()