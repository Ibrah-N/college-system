from sqlalchemy import Column, Integer, String, Sequence, Date
from sqlalchemy import ForeignKey
from app.config.db_connect import Base



class TestInfo(Base):
    __tablename__ = "test_info"

    id = Column(Integer, primary_key=True)
    center = Column(String(100))
    test_date_1 = Column(Date)
    test_date_2 = Column(Date)
    time_1 = Column(String(20))
    time_2 = Column(String(20))



class SyllabusInfo(Base):
    __tablename__ = "syllabus_info"

    syllabus_id = Column(Integer, primary_key=True)
    chemisty = Column(String(30))
    physics = Column(String(30))
    english = Column(String(30))
    general = Column(String(30))
    