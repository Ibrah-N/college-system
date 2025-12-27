from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)


from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal
from sqlalchemy import func

from app.models.admission_orm import Student
from app.models.student_enrollment_orm import StudentEnrollment
from app.models.student_fee_orm import StudentFee
from app.models.helper_orm import (Shift, ClassCode, AdmissionType,
                                    Semester, Department, Course,
                                    Session, Month, Day)


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
@student_fee_router.get("/pay_fee")
def fee_form(student_id: int, class_code_id: int,
        department_id: int, course_id: int, admission_type_id: int,
        semester_id: int, shift_id: int, request: Request, 
        db: Session = Depends(get_db)
    ):


    # === Extract Data From Form ===
    form_data = (db.query(
        Student, StudentEnrollment, ClassCode,
        Department, Course, AdmissionType, Semester, Shift
        )
        .join(StudentEnrollment, Student.student_id == StudentEnrollment.student_id)
        .join(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
        .join(Department, StudentEnrollment.department_id == Department.department_id)
        .join(Course, StudentEnrollment.course_id == Course.course_id)
        .join(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentEnrollment.semester_id == Semester.semester_id)
        .join(Shift, StudentEnrollment.shift_id == Shift.shift_id)
        .first()
        )
    form_info = {
        "student_id": form_data.StudentEnrollment.student_id,
        "student_name": form_data.Student.name,
        "father_name": form_data.Student.father_name,
        "department": form_data.Department.department_name,
        "department_id": form_data.Department.department_id,
        "course": form_data.Course.name,
        "course_id": form_data.Course.course_id,
        "shift": form_data.Shift.shift_name,
        "shift_id": form_data.Shift.shift_id,
        "class_code": form_data.ClassCode.class_code_name,
        "class_code_id": form_data.ClassCode.class_code_id,
        "admission_type": form_data.AdmissionType.admission_type,
        "admission_type_id": form_data.AdmissionType.admission_type_id,
        "semester": form_data.Semester.semester,
        "semester_id": form_data.Semester.semester_id,
        "fee": form_data.StudentEnrollment.fee
    }

    query = (
    db.query(
        Student, StudentFee, StudentEnrollment, 
        Department, Course, Shift, ClassCode,
        AdmissionType, Semester
    )
    .join(StudentFee, StudentFee.student_id == StudentEnrollment.student_id)
    .join(Student, StudentFee.student_id == Student.student_id)
    .join(Department, StudentFee.department_id == Department.department_id)
    .join(Course, StudentFee.course_id == Course.course_id)
    .join(Shift, StudentFee.shift_id == Shift.shift_id)
    .join(ClassCode, StudentFee.class_code_id == ClassCode.class_code_id)
    .join(AdmissionType, StudentFee.admission_type_id == AdmissionType.admission_type_id)
    .join(Semester, StudentFee.semester_id == Semester.semester_id)
    )
    fee_list = query.filter(
        StudentFee.student_id == student_id,
        StudentFee.class_code_id == class_code_id,
        StudentFee.department_id == department_id,
        StudentFee.course_id == course_id,
        StudentFee.admission_type_id == admission_type_id,
        StudentFee.semester_id == semester_id,
        StudentFee.shift_id == shift_id
    ).all()


    # -- if paid fee record found --
    fee_list_record = []
    if fee_list:
        for student_fee, student, enrollment, department, course, shift, classcode, admissiontype, semester in fee_list:
            fee_list_record.append({
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
                "paid": student_fee.paid,
                "discount": student_fee.discount,
                "date": student_fee.date
            })

    # -- if no record found --
    return templates.TemplateResponse(
        "pages/student_fee/student_fee_form.html",
        {
            "request": request, 
            "form_info": form_info,
            "fee_list_record": fee_list_record
        }
    )




# ============================================================
#       R E A D  -  S T U D E N T S - E N R O L M E N T.     #
# ============================================================
@student_fee_router.get("/list_fee")
def list_fee(request: Request, db: Session = Depends(get_db)):

    # -- extract record usign joins --
    result = (
    db.query(
        StudentFee.payment_id,
        Student.student_id,
        Student.name.label("student_name"),
        Student.father_name,
        Department.department_id,
        Department.department_name,
        Course.course_id,
        Course.name.label("course_name"),
        Shift.shift_id,
        Shift.shift_name,
        ClassCode.class_code_id,
        ClassCode.class_code_name,
        AdmissionType.admission_type_id,
        AdmissionType.admission_type,
        Semester.semester_id,
        Semester.semester,
        StudentEnrollment.fee,
        func.coalesce(func.sum(StudentFee.paid), 0).label("total_paid"),
        func.coalesce(func.sum(StudentFee.discount), 0).label("total_discount")
    )
    .select_from(StudentEnrollment)
    .outerjoin(StudentFee, StudentFee.student_id == StudentEnrollment.student_id)
    .outerjoin(Student, StudentEnrollment.student_id == Student.student_id)  # ✅ JOIN STUDENT
    .outerjoin(Department, StudentEnrollment.department_id == Department.department_id)
    .outerjoin(Course, StudentEnrollment.course_id == Course.course_id)
    .outerjoin(Shift, StudentEnrollment.shift_id == Shift.shift_id)
    .outerjoin(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
    .outerjoin(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
    .outerjoin(Semester, StudentEnrollment.semester_id == Semester.semester_id)
    .group_by(
        StudentFee.payment_id,
        Student.student_id,
        Student.name,
        Student.father_name,
        Department.department_id,
        Department.department_name,
        Course.course_id,
        Course.name,
        Shift.shift_id,
        Shift.shift_name,
        ClassCode.class_code_id,
        ClassCode.class_code_name,
        AdmissionType.admission_type_id,
        AdmissionType.admission_type,
        Semester.semester_id,
        Semester.semester,
        StudentEnrollment.fee
    )
    .all()
    )


    # -- jsonify record for fastapi responses --
    student_fee_records = []
    for payment_id, student_id, student_name, father_name, \
        department_id, department_name, course_id, course_name, \
        shift_id, shift_name, class_code_id, class_code_name, admission_type_id, admission_type, semester_id, semester_name, \
        fee, total_paid, total_discount in result:

        student_fee_records.append({
            "payment_id": payment_id,
            "student_id": student_id,
            "student_name": student_name,
            "father_name": father_name,
            "department_id": department_id,
            "department": department_name,
            "course_id": course_id,
            "course": course_name,
            "shift_id": shift_id,
            "shift": shift_name,
            "class_code_id": class_code_id,
            "class_code": class_code_name,
            "admission_type_id": admission_type_id,
            "admission_type": admission_type,
            "semester_id": semester_id,
            "fee": fee,
            "semester": semester_name,
            "paid_fee": total_paid,
            "discount": total_discount
        })


    # -- return response -- 
    return templates.TemplateResponse(
        "pages/student_fee/student_fee_table.html", 
        {
            "request": request,
            "studend_fee_records": student_fee_records
        }
    )




# ============================================================
#                A D D  -  S T U D E N T - F E E             #
# ============================================================
@student_fee_router.post("/add")
async def add_student_fee(
    request: Request,
    db: Session = Depends(get_db)
    ):

    form_data = await request.form()

    student_id = int(form_data.get("student_id"))
    department_id = int(form_data.get("department_id"))
    course_id = int(form_data.get("course_id"))
    class_code_id = int(form_data.get("class_code_id"))
    admission_type_id = int(form_data.get("admission_type_id"))
    semester_id = int(form_data.get("semester_id"))
    shift_id = int(form_data.get("shift_id"))

    fee_types = form_data.getlist("fee_type[]")
    paid_fees = form_data.getlist("paid_fee[]")
    discounts = form_data.getlist("discount[]")

    print("Fee Types:", fee_types)
    print("Paid Fees:", paid_fees)
    print("Discounts:", discounts)


    # for fee_type, paid_fee, discount in zip(fee_types, paid_fees, discounts):
    #     student_fee = StudentFee(
    #         student_id=student_id,
    #         department_id=department_id,
    #         course_id=course_id,
    #         class_code_id=class_code_id,
    #         admission_type_id=admission_type_id,
    #         semester_id=semester_id,
    #         shift_id=shift_id,
    #         fee_type=fee_type,
    #         paid=int(paid_fee),
    #         discount=int(discount)
    #     )
    #     db.add(student_fee)
    # db.commit()



    return JSONResponse(
        content = {
            "message": "Student fee added successfully."
        }
    )