from sqlalchemy import Column, Float, Integer
from app.config.db_connect import Base 




class AddTeacher(Base):
    __tablename__ = "teacher"


    teacher_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    father_name = Column(String(50))
    qualification = Column(String(50))
    gender = Column(String(10)) 
    contact = Column(String(15))