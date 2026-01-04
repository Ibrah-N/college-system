from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, Date
from app.config.db_connect import Base


class InstituteIncome(Base):
    __tablename__ = "institute_income"

    income_id = Column(Integer, primary_key=True)
    income_type = Column(String(50))
    income_details = Column(String(150))
    income_from = Column(String(30))
    amount = Column(Float)
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    date = Column(Date, server_default=func.current_date())  # <-- auto by DB
