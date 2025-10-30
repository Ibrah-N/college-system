from sqlalchemy import Integer, Float, ForeignKey, Column
from app.config.db_connect import Base




class TeacherRegesitration(Base):
    __tablename__ = "teacher_registration"

    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    course_id = Column(Integer, ForeignKey("course.course_id"))
    semester_id = Column(Integer, ForeignKey("semester.semester_id"))
    salary_type_id = Column(Integer, ForeignKey("salary_type.salary_type_id"))
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    salary = Column(Float)