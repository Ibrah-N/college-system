from sqlalchemy import Integer, Float, ForeignKey, Column, Date
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base



class InstituteIncomeRecipt(Base):
    __tablename__ = "institute_expense_recipt"

    recipt_id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("institute_expense.expense_id"))
    total_discount = Column(Float, default=0.0)
    left = Column(Float, default=0.0)
    date = Column(Date, server_default=func.current_date())
						