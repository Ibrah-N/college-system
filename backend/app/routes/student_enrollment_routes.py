from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal
from app.models.student_enrollment_orm import StudentEnrollment
from app.models.helper_orm import (Shift, ClassCode, AdmissionType,
                                    Semester, Department, Course)


enrollment_router = APIRouter(prefix="/student", tags=["Student"])
templates = Jinja2Templates("frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # student_id = Column(Integer, ForeignKey("student.student_id"))
    # department_id = Column(Integer, ForeignKey("department.department_id"))
    # course_id = Column(Integer, ForeignKey("course.course_id"))
    # shift_id = Column(Integer, ForeignKey("shift.shift_id"))
    # class_code_id = Column(Integer, ForeignKey("class_code.class_code_id"))
    # admission_type_id = Column(Integer, ForeignKey("admission_type.admission_type_id"))
    # semester_id = Column(Integer, ForeignKey("semester.semester_id"))
    # fee = Column(Float)

# ============================================================
#  L O A D - S T U D E N T S - E N R O L M E N T - F O R M   #
# ============================================================
@enrollment_router.get("/enrollment")
def enrollment_form(request: Request):
    return templates.TemplateResponse("pages/student/student_enrollment.html", {"request": request})

# ============================================================
#       R E A D  -  S T U D E N T S - E N R O L M E N T.     #
# ============================================================
# ============================================================
#       A D D  -  S T U D E N T - E N R O L M E N T          #
# ============================================================
# ============================================================
#    D E L E T E  -  S T U D E N T - E N R O L M E N T       #
# ============================================================
# ============================================================
#     S E A R C H -  S T U D E N T - E N R O L M E N T        #
# ============================================================
# ============================================================
#    E X P O R T -  S T U D E N T - E N R O L M E N T       #
# ============================================================



