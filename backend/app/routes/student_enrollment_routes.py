from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal

from app.models.admission_orm import Student
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


# ============================================================
#  L O A D - S T U D E N T S - E N R O L M E N T - F O R M   #
# ============================================================
@enrollment_router.get("/enrollment")
def enrollment_form(request: Request):
    return templates.TemplateResponse("pages/student/student_enrollment.html", {"request": request})


# ============================================================
#       R E A D  -  S T U D E N T S - E N R O L M E N T.     #
# ============================================================
@enrollment_router.get("/list_enrolled")
def list_enrolled(db: Session = Depends(get_db)):
    pass


# ============================================================
#       A D D  -  S T U D E N T - E N R O L M E N T          #
# ============================================================
@enrollment_router.post("/add_enrollment")
async def add_enrollment(request: Request, db : Session = Depends(get_db)):
    form_data = await request.form()

    # -- check whether ID student enrolled --
    admission = db.query(Student).filter(Student.student_id==form_data.get("student_id"))
    if not admission:
        return JSONResponse(content={
            "message": f"The student with ID {form_data.get("student_id")} not found in the in admission"
        })

    # -- add enrollment --
    new_enrollment = StudentEnrollment(
        student_id=form_data.get("student_id"), department_id=form_data.get("department"),
        course_id=form_data.get("course"), shift_id=form_data.get("course"),
        class_code_id=form_data.get("class_code"), admission_type_id=form_data.get("admission_type"),
        semester_id=form_data.get("semester"), fee=form_data.get("fee")
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return JSONResponse(content={
        "message": "Student Enrolled"
    })


# ============================================================
#    D E L E T E  -  S T U D E N T - E N R O L M E N T       #
# ============================================================
# ============================================================
#     S E A R C H -  S T U D E N T - E N R O L M E N T        #
# ============================================================
# ============================================================
#    E X P O R T -  S T U D E N T - E N R O L M E N T       #
# ============================================================



