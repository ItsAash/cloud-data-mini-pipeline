from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    engine = create_engine(
        os.getenv("DB_HOST_URI")
    )

    with engine.begin() as conn:
        with open("sql/schema.sql", "r") as f:
            conn.execute(text(f.read()))