from sqlalchemy import Column, Integer, String, Sequence, Date, func
from sqlalchemy import ForeignKey
from app.config.db_connect import Base


class DocsManagement(Base):
    __tablename__ = "docs_managment"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    doc_type_id = Column(Integer, ForeignKey("doc_type.doc_type_id"))
    doc_number = Column(String(50))
    recived_by = Column(String(100))
    reciver_phone = Column(String(15))
    doc_note = Column(String(150))
    date = Column(Date, server_default=func.current_date())
