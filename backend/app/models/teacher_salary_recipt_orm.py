from sqlalchemy import Integer, Float, ForeignKey, Column, Date
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base



class TeacherSalaryRecipt(Base):
    __tablename__ = "teacher_salary_recipt"

    recipt_id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("teacher_payment.payment_id"))
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"))
    tatal_paid = Column(Float, default=0.0)
    total_dedection = Column(Float, default=0.0)
    left = Column(Float, default=0.0)
    date = Column(Date, server_default=func.current_date())