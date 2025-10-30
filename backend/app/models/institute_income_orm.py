from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.config.db_connect import Base


class InstituteIncome(Base):
    __tablename__ = "institute_income"

    income_id = Column(Integer, primary_key=True)
    income_type = Column(String(50))
    details = Column(String(150))
    income_from = Column(String(30))
    amount = Column(Float)
    date = Column(Date)
