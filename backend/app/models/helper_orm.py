from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import ForeignKey
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


# -- course table --
class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True)
    name = Column(String(70))
    department_id = Column(Integer, ForeignKey("department.department_id"))


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
    payment_type_name = Column(String(50))



# -- salary type table --
class SalaryType(Base):
    __tablename__ = "salary_type"

    salary_type_id = Column(Integer, primary_key=True)
    salary_type_name = Column(String(15))



# -- contract type table --
class ContractType(Base):
    __tablename__ = "contract_type"

    contract_type_id = Column(Integer, primary_key=True)
    contract_type_name = Column(String(20))
    


class Session(Base):
    __tablename__ = "session"

    session_id = Column(Integer, Sequence('session_id_seq', start=24, increment=1), primary_key=True)
    session = Column(String("12"))


class Month(Base):
    __tablename__ = "month"
    
    month_id = Column(Integer, primary_key=True)
    month = Column(String(10))


class Day(Base):
    __tablename__ = "day"

    day_id = Column(Integer, primary_key=True)
    day = Column(String(3))



class DocType(Base):
    __tablename__ = "doc_type"

    doc_type_id = Column(Integer, primary_key=True)
    doc_type_name = Column(String(100))