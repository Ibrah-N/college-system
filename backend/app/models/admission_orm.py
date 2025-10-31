from sqlalchemy import Column, Integer, String, Date
from app.config.db_connect import Base


class Student(Base):
    __tablename__ = "student"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    father_name = Column(String(50))
    gender = Column(String(10))  # e.g., 'Male', 'Female', 'Other'
    date_of_birth = Column(Date) # year-month-day
    nationality = Column(String(50))
    cnic = Column(String(20))
    mobile = Column(String(15))
    emergency = Column(String(15))
    temporary_address = Column(String(200))
    permanent_address = Column(String(200))
    degree = Column(String(100))
    year = Column(Integer) 
    name_of_institute = Column(String(200))
    grade = Column(String(10))
