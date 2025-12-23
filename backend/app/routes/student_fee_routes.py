from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)


from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal

from app.models.admission_orm import Student
from app.models.student_enrollment_orm import StudentEnrollment
from app.models.helper_orm import (Shift, ClassCode, AdmissionType,
                                    Semester, Department, Course)


student_fee_router = APIRouter(prefix="/student_fee", tags=["Fee"])
templates = Jinja2Templates("frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================================#
#  L O A D - S T U D E N T S - F E E - F O R M   #
# ===============================================#
# @student_fee_router.get("/fee_form")
# def enrollment_form(request: Request):
#     return templates.TemplateResponse("pages/student_fee/student_fee_form.html", {"request": request})



# ============================================================
#       R E A D  -  S T U D E N T S - E N R O L M E N T.     #
# ============================================================
@student_fee_router.get("/list_fee")
def list_fee(request: Request, db: Session = Depends(get_db)):

    # -- extract record usign joins --
    result = (
        db.query(StudentFee, StudentEnrollment, Student, Department, Course, 
                Shift, ClassCode, AdmissionType, Semester, Session, Month, Day, 
                PaymentTypeId
                )
        .join(Student, StudentFee.student_id == Student.student_id)
        .join(Department, StudentFee.department_id == Department.department_id)
        .join(Course, StudentFee.course_id == Course.course_id)
        .join(Shift, StudentFee.shift_id == Shift.shift_id)
        .join(ClassCode, StudentFee.class_code_id == ClassCode.class_code_id)
        .join(AdmissionType, StudentFee.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentFee.semester_id == Semester.semester_id)
        .all()
    )

    session_id = Column(Integer, ForeignKey("session.session_id"))
    month_id = Column(Integer, ForeignKey("month.month_id"))
    day_id = Column(Integer, ForeignKey("day.day_id"))
    payment_type_id = Column(Integer, ForeignKey("class_code.payment_type_id"))
    paid = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    date = Column(Date, server_default=func.current_date())

    # -- jsonify record for fastapi responses --
    enrollment_data = []
    for enrollment, student, department, course, shift, classcode, admissiontype, semester in result:
        enrollment_data.append({
            "student_id": enrollment.student_id,
            "student_name": student.name,
            "father_name": student.father_name,
            "department": department.department_name,
            "department_id": department.department_id,
            "course": course.name,
            "course_id": course.course_id,
            "shift": shift.shift_name,
            "shift_id": shift.shift_id,
            "class_code": classcode.class_code_name,
            "class_code_id": classcode.class_code_id,
            "admission_type": admissiontype.admission_type,
            "admission_type_id": admissiontype.admission_type_id,
            "semester": semester.semester,
            "semester_id": semester.semester_id,
            "fee": enrollment.fee
        })

    # -- return response -- 
    return templates.TemplateResponse(
        "pages/student/student_enrollment_table.html", 
        {
            "request": request,
            "enrollment": enrollment_data
        }
    )
