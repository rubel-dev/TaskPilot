from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/taskflow_db1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind= engine
)
Base = declarative_base()