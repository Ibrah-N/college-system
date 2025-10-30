from sqlalchemy import Column, Integer, String
from app.config.db_connect import Base


# -- admission type table --
class AdmissionType(Base):
    __tablename__ = "admission_type"

    admission_type_id = Column(Integer, primary_key=True)
    admission_type = Column(String(50))



# -- semester table --
class Semester(Base):
    __tablename__ = "semester"

    semester_id = Column(Integer, primary_key=True)
    semester = Column(String(50))



# -- department table --
class Department(Base):
    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(100))



# -- IT courses table --
class ITCourse(Base):
    __tablename__ = "it_course"

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(100))



# -- short course table --
class ShortCourse(Base):
    __tablename__ = "short_course"

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(100))


# -- medical courses table --
class MedicalCourse(Base):
    __tablename__ = "medical_course"

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(100))



# -- shift table --
class Shift(Base):
    __tablename__ = "shift"

    shift_id = Column(Integer, primary_key=True)
    shift_name = Column(String(20))



# -- class code table --
class ClassCode(Base):
    __tablename__ = "class_code"

    class_code_id = Column(Integer, primary_key=True)
    class_code_name = Column(String(15))



# -- payment type --
class PaymentType(Base):
    __tablename__ = "payment_type"

    payment_type_id = Column(Integer, primary_key=True)
    payment_type_name = Column(String(15), primary_key=True)



# -- salary type table --
class SalaryType(Base):
    __tablename__ = "salary_type"

    salary_type_id = Column(Integer, primary_key=True)
    salary_type_name = Column(String(15))

    