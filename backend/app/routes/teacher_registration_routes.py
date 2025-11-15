from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)

import pandas as pd
import io

from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal

from app.models.teacher_registration_orm import TeacherRegesitration
from app.models.add_teacher_orm import AddTeacher
from app.models.helper_orm import (Department, Course, Shift,
                                    SalaryType, Semester)


teacher_registration_router = APIRouter(prefix="/teacher", tags=['Teacher'])
templates = Jinja2Templates("frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================================================================
#  L O A D - T E A C H E R - R E G I S T R A T I O N - F O R M   #
# ================================================================
@teacher_registration_router.get("/registration")
def teacher_registration(request: Request):
    return templates.TemplateResponse(
        "pages/teacher/teacher_registration.html",
        {
            "request": request
        }
    )


# ================================================================
#       R E A D  -  T E A C H E R - R E G I S T R A T I O N      #
# ================================================================
@teacher_registration_router.get("/list_registration")
def list_registration(request: Request, db: Session = Depends(get_db)):

    # -- extract record usign joins --
    result = (
        db.query(TeacherRegesitration, AddTeacher, Department,
                Course, Shift, SalaryType, Semester
                )
        .join(AddTeacher, TeacherRegesitration.teacher_id == AddTeacher.teacher_id)
        .join(Department, TeacherRegesitration.department_id == Department.department_id)
        .join(Course, TeacherRegesitration.course_id == Course.course_id)
        .join(Shift, TeacherRegesitration.shift_id == Shift.shift_id)
        .join(SalaryType, TeacherRegesitration.salary_type_id == SalaryType.salary_type_id)
        .join(Semester, TeacherRegesitration.semester_id == Semester.semester_id)
        .all()
    )

    # -- jsonify record for fastapi responses --
    registration_data = []
    for registration, add_teacher, department, course, shift, salary_type, semester in result:
        registration_data.append({
            "teacher_id": registration.teacher_id,
            "teacher_name": add_teacher.name,
            "father_name": add_teacher.father_name,
            "department": department.department_name,
            "department_id": department.department_id,
            "course": course.name,
            "course_id": course.course_id,
            "shift": shift.shift_name,
            "shift_id": shift.shift_id,
            "salary_type": salary_type.salary_type_name,
            "salary_type_id": salary_type.salary_type_id,
            "semester": semester.semester,
            "semester_id": semester.semester_id,
            "salary": registration.salary
        })

    # -- return response -- 
    return templates.TemplateResponse(
        "pages/teacher/teacher_registration_table.html", 
        {
            "request": request,
            "registrations": registration_data
        }
    )

    
# ================================================================
#       A D D  -  T E A C H E R - R E G I S T R A T I O N        #
# ================================================================
@teacher_registration_router.post("/register_teacher")
async def register_teacher(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    # -- check teacher existance --
    teacher = db.query(AddTeacher).filter(
        AddTeacher.teacher_id==int(form_data.get("teacher_id"))
    ).first()
    if not teacher:
        return JSONResponse(
            content = {
                "message": "Teacher is not added!!"
            }, status_code=404
        )

    # -- check teacher registration --
    teacher_registration = db.query(TeacherRegesitration).filter(
        TeacherRegesitration.teacher_id==int(form_data.get("teacher_id")),
        TeacherRegesitration.department_id==int(form_data.get("department_id")),
        TeacherRegesitration.course_id==int(form_data.get("course_id")),
        TeacherRegesitration.semester_id==int(form_data.get("semester_id")),
        TeacherRegesitration.salary_type_id==int(form_data.get("salary_type_id")),
        TeacherRegesitration.shift_id==int(form_data.get("shift_id"))
    ).first()
    if teacher_registration:
        return JSONResponse(
            content = {
                "message": "Teacher Registration Already Exists"
            }, status_code=409
        )

    # -- new registration --
    new_registration = TeacherRegesitration(
        teacher_id=form_data.get("teacher_id"), department_id=form_data.get("department_id"),
        course_id=form_data.get("course_id"), shift_id=form_data.get("shift_id"),
        salary_type_id=form_data.get("salary_type_id"), semester_id=form_data.get("semester_id"),
        salary=form_data.get("salary")
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    
    # -- response --
    return RedirectResponse(
        url="/teacher/list_registration",
        status_code=303
    )

# ================================================================
#    D E L E T E  -  T E A C H E R - R E G I S T R A T I O N     #
# ================================================================
@teacher_registration_router.delete("/delete_registration")
def delete_registration(
    teacher_id: int, department_id: int, 
    course_id: int, salary_type_id: int,
    semester_id: int, shift_id: int, 
    db: Session = Depends(get_db)
    ):

    # -- filter registration --
    registration = db.query(TeacherRegesitration).filter_by(
        teacher_id=teacher_id,
        department_id=department_id,
        course_id=course_id,
        salary_type_id=salary_type_id,
        semester_id=semester_id, 
        shift_id=shift_id
    ).first()

    # -- existance check --
    if not registration:
        return JSONResponse(
            content = {
                "message": "Registration not found!!"
            }, status_code = 404
        )

    # -- delete ---
    db.delete(registration)
    db.commit()

    # -- response --
    return RedirectResponse(
        url="/teacher/list_registration",
        status_code=303
    )

# ================================================================
#     S E A R C H -  T E A C H E R - R E G I S T R A T I O N     #
# ================================================================
@teacher_registration_router.post("/registration_search")
async def registration_search(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()

    # -- extract join data --
    query = (
        db.query(TeacherRegesitration, AddTeacher, Department,
                Course, Shift, SalaryType, Semester
                )
        .join(AddTeacher, TeacherRegesitration.teacher_id == AddTeacher.teacher_id)
        .join(Department, TeacherRegesitration.department_id == Department.department_id)
        .join(Course, TeacherRegesitration.course_id == Course.course_id)
        .join(Shift, TeacherRegesitration.shift_id == Shift.shift_id)
        .join(SalaryType, TeacherRegesitration.salary_type_id == SalaryType.salary_type_id)
        .join(Semester, TeacherRegesitration.semester_id == Semester.semester_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            TeacherRegesitration.teacher_id==int(form_data.get("id_search"))
        )
        result = query.all()
        # -- jsonify --
        registration_data = []
        for registration, add_teacher, department, course, shift, salary_type, semester in result:
            registration_data.append({
                "teacher_id": registration.teacher_id,
                "teacher_name": add_teacher.name,
                "father_name": add_teacher.father_name,
                "department": department.department_name,
                "department_id": department.department_id,
                "course": course.name,
                "course_id": course.course_id,
                "shift": shift.shift_name,
                "shift_id": shift.shift_id,
                "salary_type": salary_type.salary_type_name,
                "salary_type_id": salary_type.salary_type_id,
                "semester": semester.semester,
                "semester_id": semester.semester_id,
                "salary": registration.salary
            })
        # -- response --
        return templates.TemplateResponse(
            "pages/teacher/teacher_registration_table.html",
            {
                "request": request,
                "registrations": registration_data
            }
        )

    # -- name search --
    if form_data.get("name_search"):
        query = query.filter(
            AddTeacher.name.ilike(f"%{form_data.get("name_search")}%")
        )
    # -- department search --
    if form_data.get("department_id"):
        query = query.filter(
            TeacherRegesitration.department_id==int(form_data.get("department_id"))
        )
    # -- course search --
    if form_data.get("course_id"):
        query = query.filter(
            TeacherRegesitration.course_id==int(form_data.get("course_id"))
        )
    # -- salary type search --
    if form_data.get("salary_type_id"):
        query = query.filter(
            TeacherRegesitration.salary_type_id==int(form_data.get('salary_type_id'))
        )
    # -- semester search --
    if form_data.get("semester_id"):
        query = query.filter(
            TeacherRegesitration.semester_id==int(form_data.get("semester_id"))
        )
    # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            TeacherRegesitration.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    registration_data = []
    for registration, add_teacher, department, course, shift, salary_type, semester in result:
        registration_data.append({
            "teacher_id": registration.teacher_id,
            "teacher_name": add_teacher.name,
            "father_name": add_teacher.father_name,
            "department": department.department_name,
            "department_id": department.department_id,
            "course": course.name,
            "course_id": course.course_id,
            "shift": shift.shift_name,
            "shift_id": shift.shift_id,
            "salary_type": salary_type.salary_type_name,
            "salary_type_id": salary_type.salary_type_id,
            "semester": semester.semester,
            "semester_id": semester.semester_id,
            "salary": registration.salary
        })

    # -- response --
    return templates.TemplateResponse(
        "pages/teacher/teacher_registration_table.html",
        {
            "request": request,
            "registrations": registration_data
        }
    )


    

# ================================================================
#    E X P O R T -  T E A C H E R - R E G I S T R A T I O N      #
# ================================================================
@teacher_registration_router.post("/export_registration")
async def export_registration(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()


    # -- extract join data --
    query = (
        db.query(TeacherRegesitration, AddTeacher, Department,
                Course, Shift, SalaryType, Semester
                )
        .join(AddTeacher, TeacherRegesitration.teacher_id == AddTeacher.teacher_id)
        .join(Department, TeacherRegesitration.department_id == Department.department_id)
        .join(Course, TeacherRegesitration.course_id == Course.course_id)
        .join(Shift, TeacherRegesitration.shift_id == Shift.shift_id)
        .join(SalaryType, TeacherRegesitration.salary_type_id == SalaryType.salary_type_id)
        .join(Semester, TeacherRegesitration.semester_id == Semester.semester_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            TeacherRegesitration.teacher_id==int(form_data.get("id_search"))
        )
        result = query.all()
        # -- jsonify --
        registration_data = []
        for registration, add_teacher, department, course, shift, salary_type, semester in result:
            registration_data.append({
                "teacher_id": registration.teacher_id,
                "teacher_name": add_teacher.name,
                "father_name": add_teacher.father_name,
                "department": department.department_name,
                "course": course.name,
                "shift": shift.shift_name,
                "salary_type": salary_type.salary_type_name,
                "semester": semester.semester,
                "salary": registration.salary
            })
        
        # -- write csv --
        df = pd.DataFrame(registration_data)

        # -- export csv --
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        # -- response --
        return StreamingResponse(
            buffer,
            media_type = "text/csv",
            headers = {
                "Content-Disposition": "attachment; filename=registration_export.csv"
            }
        )


    # -- name search --
    if form_data.get("name_search"):
        query = query.filter(
            AddTeacher.name.ilike(f"%{form_data.get("name_search")}%")
        )
    # -- department search --
    if form_data.get("department_id"):
        query = query.filter(
            TeacherRegesitration.department_id==int(form_data.get("department_id"))
        )
    # -- course search --
    if form_data.get("course_id"):
        query = query.filter(
            TeacherRegesitration.course_id==int(form_data.get("course_id"))
        )
    # -- salary type search --
    if form_data.get("salary_type_id"):
        query = query.filter(
            TeacherRegesitration.salary_type_id==int(form_data.get('salary_type_id'))
        )
    # -- semester search --
    if form_data.get("semester_id"):
        query = query.filter(
            TeacherRegesitration.semester_id==int(form_data.get("semester_id"))
        )
    # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            TeacherRegesitration.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    registration_data = []
    for registration, add_teacher, department, course, shift, salary_type, semester in result:
        registration_data.append({
            "teacher_id": registration.teacher_id,
            "teacher_name": add_teacher.name,
            "father_name": add_teacher.father_name,
            "department": department.department_name,
            "course": course.name,
            "shift": shift.shift_name,
            "salary_type": salary_type.salary_type_name,
            "semester": semester.semester,
            "salary": registration.salary
        })

    # -- write csv --
    df = pd.DataFrame(registration_data)

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer, 
        media_type = "text/csv",
        headers = {
            "Content-Disposition": "attachment; filename=registration_export.csv"
        }
    )

