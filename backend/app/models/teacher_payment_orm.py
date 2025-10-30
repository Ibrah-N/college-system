from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.config.db_connect import Base



class TeacherPayment(Base):
    __tablename__ = "teacher_payment"

    payment_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    course_id = Column(Integer, ForeignKey("course.course_id"))
    semester_id = Column(Integer, ForeignKey("semester.semester_id"))
    salary_type_id = Column(Integer, ForeignKey("salary_type.salary_type_id"))
    paid_salary = Column(Float)
    deduction = Column(Float, default=0.0)
    date = Column(Date)


