from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base


class StudentEnrollment(Base):
    __tablename__ = "student_enrollment"

    student_id = Column(Integer, ForeignKey("student.student_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    course_id = Column(Integer, ForeignKey("course.course_id"))
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    class_code_id = Column(Integer, ForeignKey("class_code.class_code_id"))
    admission_type_id = Column(Integer, ForeignKey("admission_type.admission_type_id"))
    semester_id = Column(Integer, ForeignKey("semester.semester_id"))
    fee = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "student_id",
            "department_id",
            "course_id",
            "shift_id",
            "class_code_id",
            "admission_type_id",
            "semester_id",
            name="pk_student_enrollment"
        ),
    )
