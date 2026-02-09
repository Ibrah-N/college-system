from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# -- local development --
# DATABASE_URL = "postgresql://ibrahim@localhost/college_system"
# engine = create_engine(DATABASE_URL)

# -- env vars --
DATABASE_URL = os.environ["DATABASE_URL"]

# -- docker development --
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
