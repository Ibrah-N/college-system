from sqlalchemy import Integer, Float, ForeignKey, Column
from sqlalchemy.schema import PrimaryKeyConstraint
from app.config.db_connect import Base





class TeacherRegesitration(Base):
    __tablename__ = "teacher_registration"

    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    contract_type_id = Column(Integer, ForeignKey("contract_type.contract_type_id"))
    shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    salary = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "teacher_id",
            "department_id",
            "contract_type_id",
            "shift_id",
            name="pk_teacher_registration"
        ),
    )