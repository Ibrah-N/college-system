from sqlalchemy import Integer, Float, ForeignKey, Column, Date
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base
from sqlalchemy import func



class StudentFee(Base):
    __tablename__ = "student_fee"

    payment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    course_id = Column(Integer, ForeignKey("course.course_id"))
    admission_type_id = Column(Integer, ForeignKey("admission_type.admission_type_id"))
    semester_id = Column(Integer, ForeignKey("semester.semester_id"))
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    class_code_id = Column(Integer, ForeignKey("class_code.class_code_id"))
    fee_type_id = Column(Integer, ForeignKey("payment_type.payment_type_id"))
    paid = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    date = Column(Date, server_default=func.current_date())
													
													
																											