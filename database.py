from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create the database file (we'll start with SQLite for easy setup, then move to Postgres)
SQLALCHEMY_DATABASE_URL = "sqlite:///./smart_clothing.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define our "Sales" Table
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    sku = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

# 3. Create the tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)