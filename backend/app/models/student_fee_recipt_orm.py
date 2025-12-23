from sqlalchemy import Integer, Float, ForeignKey, Column, Date
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base



class StudentFeeRecipt(Base):
    __tablename__ = "student_fee_recipt"

    recipt_id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("student_fee.payment_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"))
    total_paid = Column(Float, default=0.0)
    total_discount = Column(Float, default=0.0)
    left = Column(Float, default=0.0)
    date = Column(Date, server_default=func.current_date())
						
						