from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.config.db_connect import Base





class InstituteExpense(Base):
    __tablename__ = "institute_expense"

    expense_id = Column(Integer, primary_key=True)
    item_detail = Column(String(50))
    expense_for = Column(String(150))
    expense_by = Column(String(30))
    amount = Column(Float)
    date = Column(Date)
