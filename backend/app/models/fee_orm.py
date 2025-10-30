from sqlalchemy import Column, String, Integer, Float ForeignKey
from app.config.db_connect import Base




class Fee(Base):
    __tablename__ = "fee"

    payment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    department_id = Column(Integer, ForeginKey("department.department_id"))
    course_id = Column(Integer, ForeginKey("course.course_id"))
    shift_id = Column(Integer, ForeginKey("shift.shift_id"))
    class_code_id = Column(Integer, ForeginKey("class_code.class_code_id"))
    admission_type_id = Column(Integer, ForeginKey("admission_type.admission_type_id"))
    semester_id = Column(Integer, ForeginKey("semester.semester_id"))
    payment_type_id = Column(Integer, ForeginKey("payment_type.payment_type_id"))
    paid_fee = Column(Float)
    discount = Column(Float)
    date = Column(Date)
