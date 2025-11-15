from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, Date
from app.config.db_connect import Base


class InstituteIncome(Base):
    __tablename__ = "institute_income"

    income_id = Column(Integer, primary_key=True)
    income_type = Column(String(50))
    details = Column(String(150))
    income_from = Column(String(30))
    amount = Column(Float)
    session = Column(Integer, ForeignKey("session.session_id"))
    month = Column(Integer, ForeignKey("month.month_id"))
    day = Column(Integer, ForeignKey("day.day_id"))
    date = Column(Date, server_default=func.current_date())  # <-- auto by DB
