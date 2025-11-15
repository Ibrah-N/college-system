from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, Date
from app.config.db_connect import Base





class InstituteExpense(Base):
    __tablename__ = "institute_expense"

    expense_id = Column(Integer, primary_key=True)
    item_detail = Column(String(50))
    expense_for = Column(String(150))
    expense_by = Column(String(30))
    amount = Column(Float)
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    session_id = Column(Integer, ForeignKey("session.session_id"))
    month_id = Column(Integer, ForeignKey("month.month_id"))
    day_id = Column(Integer, ForeignKey("day.day_id"))
    date = Column(Date, server_default=func.current_date())  # <-- auto by DB