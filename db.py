from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "sqlite:///todosapp.db"
DATABASE_URL = "postgresql://postgres:PavitarKhushi@db.bllnaolmucjcmqdfmrvj.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
