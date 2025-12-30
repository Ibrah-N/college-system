from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse, Response,
                                RedirectResponse, StreamingResponse)

from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal
from sqlalchemy import func, and_




from app.models.teacher_payment_orm import TeacherPayment
from app.models.add_teacher_orm import AddTeacher
from app.models.teacher_registration_orm import TeacherRegesitration
from app.models.helper_orm import (Department, Course, Shift
                                    Semester, SalaryType)




teacher_salary_router = APIRouter(prefix="/salary", tags=["SALARY"])
templates = Jinja2Templates("frontend")


# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# ============================================================
#       R E A D  -  T E A C H E R - S A L A R Y              #
# ============================================================
@teacher_salary_router.get("/list_salary")
def list_salary(request: Request, db: Session = Depends(get_db)):
    """
    teacher_id,
    Teacher_Name
    Father_name
    Department
    Course
    Salary Type
    Salary
    Paid
    Deduction
    """
        # -- extract record using joins --
    result = (
    db.query(
        TeacherRegesitration.teacher_id,

        AddTeacher.name.label("teacher_name"),
        AddTeacher.father_name,

        Department.department_id,
        Department.department_name,

        Course.course_id,
        Course.name.label("course_name"),

        Shift.shift_id,
        Shift.shift_name,

        SalaryType.salary_type_id,
        SalaryType.salary_type_name,

        TeacherRegesitration.salary,

        func.coalesce(func.sum(TeacherPayment.paid_salary), 0).label("paid_salary"),
        func.coalesce(func.sum(TeacherPayment.deduction), 0).label("deduction"),
    )
    .select_from(TeacherRegesitration)   # BASE TABLE

    .join(AddTeacher, AddTeacher.teacher_id == TeacherRegesitration.teacher_id)
    .join(Department, Department.department_id == TeacherRegesitration.department_id)
    .join(Course, Course.course_id == TeacherRegesitration.course_id)
    .join(Shift, Shift.shift_id == TeacherRegesitration.shift_id)

    #  CORRECT LEFT JOIN (IMPORTANT)
    .outerjoin(
        TeacherPayment,
        and_(
            TeacherPayment.teacher_id == TeacherRegesitration.teacher_id,
            TeacherPayment.department_id == TeacherRegesitration.department_id,
            TeacherPayment.course_id == TeacherRegesitration.course_id,
            TeacherPayment.shift_id == TeacherRegesitration.shift_id,
        )
    )
    .group_by(
        TeacherRegesitration.teacher_id,
        AddTeacher.name,
        AddTeacher.father_name,
        Department.department_id,
        Department.department_name,
        Course.course_id,
        Course.name,
        Shift.shift_id,
        Shift.shift_name,
        SalaryType.salary_type_id,
        SalaryType.salary_type_name,
        TeacherRegesitration.salary,
    )
    .all()
    )


        # -- jsonify record for fastapi responses --
    teacher_salary_record = []
    for teacher_id, teacher_name, father_name, \
        department_id, department_name, course_id, course_name, \
        shift_id, shift_name, salary_type_id, salary_type_name, \
        salary, paid_salary, deduction in result:

        student_fee_records.append({
            "teacher_id": student_id,
            "teacher_name": student_name,
            "father_name": father_name,
            "department_id": department_id,
            "department": department_name,
            "course_id": course_id,
            "course": course_name,
            "shift_id": shift_id,
            "shift": shift_name,
            "salary_type_id": salary_type_id,
            "salary_type_name": salary_type_name
            "salary": salary,
            "paid_salary": paid_salary,
            "deduction": deduction
        })


    print(teacher_salary_record)