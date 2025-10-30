from sqlalchemy import Column, Float, Integer, ForeignKey
from app.config.db_connect import Base 



session	month	total_fee	due_fee	paid_salary	due_salary	instt_income	
instt_expense	total_income	total_expenses	account


class Account(Base):
    session_id = Column(Integer, ForeignKey("session.session_id"))
    month_id = Column(Integer, ForeignKey("month.month_id"))
    day_id = Column(Integer, ForeignKey("day.day_id"))
    total_fee = Column(Float)
    due_fee = Column(Float)
    paid_salary = Column(Float)
    due_salary = Column(Float)
    instt_income = Column(Float)
    instt_expense = Column(Float)
    total_income = Column(Float)
    total_expenses = Column(Float)
    account = Column(Float)