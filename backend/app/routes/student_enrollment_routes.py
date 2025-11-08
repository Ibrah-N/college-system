from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)
import pandas as pd
import io

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
def list_enrolled(request: Request, db: Session = Depends(get_db)):

    # -- extract record usign joins --
    result = (
        db.query(StudentEnrollment, Student, Department, Course, 
                Shift, ClassCode, AdmissionType, Semester
                )
        .join(Student, StudentEnrollment.student_id == Student.student_id)
        .join(Department, StudentEnrollment.department_id == Department.department_id)
        .join(Course, StudentEnrollment.course_id == Course.course_id)
        .join(Shift, StudentEnrollment.shift_id == Shift.shift_id)
        .join(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
        .join(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentEnrollment.semester_id == Semester.semester_id)
        .all()
    )

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

    # -- check enrollment --
    enrollment = db.query(StudentEnrollment).filter_by(
        student_id=int(form_data.get("student_id")),
        class_code_id=int(form_data.get("class_code_id")),
        department_id=int(form_data.get("department_id")),
        course_id=int(form_data.get("course_id")),
        admission_type_id=int(form_data.get("admission_type_id")),
        semester_id=int(form_data.get("semester_id")),
        shift_id=int(form_data.get("shift_id"))
    ).first()
    if enrollment:
        return JSONResponse(
            content = {
                'message': "Student is already Enrolled"
            }, status_code=409
        )
    

    # -- add enrollment --
    new_enrollment = StudentEnrollment(
        student_id=form_data.get("student_id"), department_id=form_data.get("department_id"),
        course_id=form_data.get("course_id"), shift_id=form_data.get("shift_id"),
        class_code_id=form_data.get("class_code_id"), admission_type_id=form_data.get("admission_type_id"),
        semester_id=form_data.get("semester_id"), fee=form_data.get("fee")
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return RedirectResponse(
        url="/student/list_enrolled",
        status_code=303
    )


# ============================================================
#    D E L E T E  -  S T U D E N T - E N R O L M E N T       #
# ============================================================
@enrollment_router.delete("/delete_enrollment")
def delete_enrollment(student_id: int, class_code_id: int,
    department_id: int, course_id: int, admission_type_id: int,
    semester_id: int, shift_id: int, db: Session = Depends(get_db)
    ):

    enrollment = db.query(StudentEnrollment).filter_by(
        student_id=student_id,
        class_code_id=class_code_id,
        department_id=department_id,
        course_id=course_id,
        admission_type_id=admission_type_id,
        semester_id=semester_id,
        shift_id=shift_id
    ).first()

    if not enrollment:
        return JSONResponse(content={
            "message": "Student Enrollment Not Found",
        }, status_code=404)

    db.delete(enrollment)
    db.commit()
    return RedirectResponse(
        url="/student/list_enrolled",
        status_code=303
    )


# ============================================================
#     S E A R C H -  S T U D E N T - E N R O L M E N T       #
# ============================================================
@enrollment_router.post("/enrollment_search")
async def search_enrollment(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    enrollment_data = []

    # -- extract record usign joins --
    query = (
        db.query(StudentEnrollment, Student, Department, Course, 
                Shift, ClassCode, AdmissionType, Semester
                )
        .join(Student, StudentEnrollment.student_id == Student.student_id)
        .join(Department, StudentEnrollment.department_id == Department.department_id)
        .join(Course, StudentEnrollment.course_id == Course.course_id)
        .join(Shift, StudentEnrollment.shift_id == Shift.shift_id)
        .join(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
        .join(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentEnrollment.semester_id == Semester.semester_id)
    )
    # -- search filters --
    # if id-search enabled it will only search
    # on the basis of id else it will look for 
    # all other filter combinaly
    if form_data.get("id_search"):
        query = query.filter(Student.student_id==int(form_data.get("id_search")))
        result = query.all()
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

        return templates.TemplateResponse(
            "pages/student/student_enrollment_table.html", 
            {"request": request, "enrollment": enrollment_data}
        )

    print(form_data.get("name_search"))
    if form_data.get("name_search"):
        query = query.filter(Student.name.ilike(f"%{form_data.get('name_search')}%"))
    if form_data.get("class_code_id"):
        query = query.filter(ClassCode.class_code_id==int(form_data.get("class_code_id")))
    if form_data.get("department_id"):
        query = query.filter(Department.department_id==int(form_data.get("department_id")))
    if form_data.get(("course_id")):
        query = query.filter(Course.course_id==int(form_data.get("course_id")))
    if form_data.get("admission_type_id"):
        query = query.filter(AdmissionType.admission_type_id==int(form_data.get("admission_type_id")))
    if form_data.get("semester_id"):
        query = query.filter(Semester.semester_id==int(form_data.get("semester_id")))
    if form_data.get("shift_id"):
        query = query.filter(Shift.shift_id==int(form_data.get("shift_id")))
    result = query.all()

    
    # -- jsonify record for fastapi responses --
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



# ============================================================
#    E X P O R T -  S T U D E N T - E N R O L M E N T       #
# ============================================================
@enrollment_router.post("/export_enrollment")
async def export_enrollment(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    enrollment_data = []
    search_flag = False

    # -- extract record usign joins --
    query = (
        db.query(StudentEnrollment, Student, Department, Course, 
                Shift, ClassCode, AdmissionType, Semester
                )
        .join(Student, StudentEnrollment.student_id == Student.student_id)
        .join(Department, StudentEnrollment.department_id == Department.department_id)
        .join(Course, StudentEnrollment.course_id == Course.course_id)
        .join(Shift, StudentEnrollment.shift_id == Shift.shift_id)
        .join(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
        .join(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentEnrollment.semester_id == Semester.semester_id)
    )
    # -- search filters --
    # if id-search enabled it will only search
    # on the basis of id else it will look for 
    # all other filter combinaly
    if form_data.get("id_search"):
        search_flag = True
        query = query.filter(Student.student_id==int(form_data.get("id_search")))
        result = query.all()
        for enrollment, student, department, course, shift, classcode, admissiontype, semester in result:
            enrollment_data.append({
                "student_id": enrollment.student_id,
                "student_name": student.name,
                "father_name": student.father_name,
                "class_code": classcode.class_code_name,
                "department": department.department_name,
                "course": course.name,
                "admission_type": admissiontype.admission_type,
                "semester": semester.semester,
                "shift": shift.shift_name,
                "fee": enrollment.fee
            })

        # -- write csv --
        df = pd.DataFrame(enrollment_data)

        # # --- Export as Excel ---
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=enrollment_export.csv"}
        )


    # -- search filters --
    if form_data.get("name_search"):
        query = query.filter(Student.name.ilike(f"%{form_data.get('name_search')}%"))
        search_flag = True
    if form_data.get("class_code_id"):
        query = query.filter(ClassCode.class_code_id==int(form_data.get("class_code_id")))
        search_flag = True
    if form_data.get("department_id"):
        query = query.filter(Department.department_id==int(form_data.get("department_id")))
        search_flag = True
    if form_data.get(("course_id")):
        query = query.filter(Course.course_id==int(form_data.get("course_id")))
        search_flag = True
    if form_data.get("admission_type_id"):
        query = query.filter(AdmissionType.admission_type_id==int(form_data.get("admission_type_id")))
        search_flag = True
    if form_data.get("semester_id"):
        query = query.filter(Semester.semester_id==int(form_data.get("semester_id")))
        search_flag = True
    if form_data.get("shift_id"):
        query = query.filter(Shift.shift_id==int(form_data.get("shift_id")))
        search_flag = True

    result = None
    if search_flag:
        result = query.all()
    else:
        result = query.all()

    
    # -- jsonify record for fastapi responses --
    for enrollment, student, department, course, shift, classcode, admissiontype, semester in result:
        enrollment_data.append({
            "student_id": enrollment.student_id,
            "student_name": student.name,
            "father_name": student.father_name,
            "class_code": classcode.class_code_name,
            "department": department.department_name,
            "course": course.name,
            "admission_type": admissiontype.admission_type,
            "semester": semester.semester,
            "shift": shift.shift_name,
            "fee": enrollment.fee
        })

    # -- write csv --
    df = pd.DataFrame(enrollment_data)

    # # --- Export as Excel ---
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=enrollment_export.csv"}
    )

