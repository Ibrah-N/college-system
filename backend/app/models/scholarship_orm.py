from sqlalchemy import Column, Integer, String, Sequence, Date, LargeBinary
from sqlalchemy import ForeignKey
from app.config.db_connect import Base


class Scholarship(Base):
    __tablename__ = "scholarship"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"))
    name = Column(String(100))
    father_name = Column(String(100))
    qualification = Column(String(100))
    whatsapp = Column(String(20))
    current_institute = Column(String(150))
    cnic_formb = Column(String(20))
    address = Column(String(200))
    registration_date = Column(Date)
    photo_blob = Column(LargeBinary, nullable=True)
