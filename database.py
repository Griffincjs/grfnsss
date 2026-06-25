import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# --- ENVIRONMENT-AWARE DATABASE URL ---
# Locally: uses SQLite (no setup needed)
# On Render: reads the DATABASE_URL environment variable (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smart_clothing.db")

# Render provides "postgres://" but SQLAlchemy requires "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs a special thread argument; PostgreSQL does not
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SALES TABLE DEFINITION ---
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    sku = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

# --- CREATE TABLES IF THEY DON'T EXIST ---
def init_db():
    Base.metadata.create_all(bind=engine)
