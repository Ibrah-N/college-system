from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from sqlalchemy import text


from sqlalchemy import and_, extract

from app.models.admission_orm import Student
from app.models.student_enrollment_orm import StudentEnrollment
from app.models.student_fee_orm import StudentFee

from app.models.add_teacher_orm import AddTeacher
from app.models.teacher_payment_orm import TeacherPayment

from app.models.institute_expense_orm import InstituteExpense
from app.models.institute_income_orm import InstituteIncome

from app.models.helper_orm import (Shift, ClassCode, AdmissionType,
                                    Semester, Department, Course,
                                    PaymentType, SalaryType)




import pandas as pd
import io
from datetime import datetime


# -- add paths --
reports_router = APIRouter(prefix="/reports", tags=["Account"])
templates = Jinja2Templates(directory="frontend")


# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@reports_router.get("/institute_income_report")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/income_report.html",
        {
            "request": request
        }
    )


@reports_router.get("/fee_report")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/fee_report.html",
        {
            "request": request
        }
    )


@reports_router.get("/salary_report")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/salary_report.html",
        {
            "request": request
        }
    )


@reports_router.get("/institute_expense_report")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/expense_report.html",
        {
            "request": request
        }
    )


@reports_router.get("/report_01")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/report_01_table.html",
        {
            "request": request
        }
    )



def generate_salary_data(
    session_id, 
    month_id, 
    day_id, 
    db
    ):

    #  -- build base query --
    query = (
    db.query(
            TeacherPayment.payment_id,
            AddTeacher.name,
            AddTeacher.father_name,
            Department.department_name,
            SalaryType.salary_type_name,
            TeacherPayment.paid_salary,
            TeacherPayment.deduction,
            TeacherPayment.date
        )
        .join(
            TeacherPayment,
            TeacherPayment.teacher_id == AddTeacher.teacher_id
        )
        .join(
            Department,
            Department.department_id == TeacherPayment.department_id
        )
        .join(
            SalaryType,
            SalaryType.salary_type_id == TeacherPayment.salary_type_id
        )
    )

    # -- apply filters dynamically --
    if session_id:
        query = query.filter(extract("year", TeacherPayment.date) == int("20"+session_id))
    if month_id and month_id.isdigit():
        query = query.filter(extract("month", TeacherPayment.date) == int(month_id))
    if day_id and day_id.isdigit():
        query = query.filter(extract("day", TeacherPayment.date) == int(day_id))

    # -- execute query --
    results = query.order_by(TeacherPayment.date).all()

    # -- jesonify response --
    data = []
    for row in results:
        data.append({
            "payment_id": row.payment_id,
            "name": row.name,
            "father_name": row.father_name,
            "department_name": row.department_name,
            "salary_type_name": row.salary_type_name,
            "paid_salary": row.paid_salary,
            "deduction": row.deduction,
            "date": row.date.strftime("%Y-%m-%d")
        })

    #   -- write csv --
    df = pd.DataFrame(data)
    if df.shape[0] > 0:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df["date"] = df["date"].apply(
        lambda x: f"{x.year}-{x.strftime('%b').lower()}-{x.day}")

    # -- return data  --
    return df



def generate_expense_data(
    session_id, 
    month_id, 
    day_id, 
    db
    ):

    #  -- build base query --
    query = (
        db.query(
            InstituteExpense.expense_id,
            InstituteExpense.item_detail,
            InstituteExpense.expense_for,
            InstituteExpense.expense_by,
            InstituteExpense.amount,
            InstituteExpense.date
        )
    )
    # -- apply filters dynamically --
    if session_id:
        query = query.filter(extract("year", InstituteExpense.date) == int("20"+session_id))
    if month_id and month_id.isdigit():
        query = query.filter(extract("month", InstituteExpense.date) == int(month_id))
    if day_id and day_id.isdigit():
        query = query.filter(extract("day", InstituteExpense.date) == int(day_id))
    
    # -- execute query --
    results = query.order_by(InstituteExpense.date).all()

    # -- jesonify response --
    data = []
    for row in results:
        data.append({
            "expense_id": row.expense_id,
            "item_detail": row.item_detail,
            "expense_for": row.expense_for,
            "expense_by": row.expense_by,
            "amount": row.amount,
            "date": row.date.strftime("%Y-%m-%d")
        })

    #   -- write csv --
    df = pd.DataFrame(data)
    if df.shape[0] > 0:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df["date"] = df["date"].apply(
        lambda x: f"{x.year}-{x.strftime('%b').lower()}-{x.day}")
    
    # -- return data  --
    return df



def generate_fee_data(
    session_id, 
    month_id, 
    day_id, 
    db   
    ):

    # -- extract filters --
    query = (
        db.query(
            StudentFee.payment_id,
            Student.name.label("student_name"),
            Student.father_name,
            Department.department_name,
            Course.name,
            StudentFee.paid,
            StudentFee.discount,
            StudentFee.date
        )
        .join(
            StudentEnrollment,
            StudentEnrollment.student_id == Student.student_id
        )
        .join(
            StudentFee,
            and_(
                StudentFee.student_id == StudentEnrollment.student_id,
                StudentFee.department_id == StudentEnrollment.department_id,
                StudentFee.course_id == StudentEnrollment.course_id,
                StudentFee.admission_type_id == StudentEnrollment.admission_type_id,
                StudentFee.shift_id == StudentEnrollment.shift_id,
                StudentFee.class_code_id == StudentEnrollment.class_code_id
            )
        )
        .join(
            Department,
            Department.department_id == StudentFee.department_id
        )
        .join(
            Course,
            Course.course_id == StudentFee.course_id
        )
    )

    # -- apply filters dynamically --
    if session_id:
        query = query.filter(extract("year", StudentFee.date) == int("20"+session_id))
    if month_id and month_id.isdigit():
        query = query.filter(extract("month", StudentFee.date) == int(month_id))
    if day_id and day_id.isdigit():
        query = query.filter(extract("day", StudentFee.date) == int(day_id))

    # -- execute query --
    results = query.order_by(StudentFee.date).all()

    # -- jesonify response --
    data = []
    for row in results:
        data.append({
            "payment_id": row.payment_id,
            "name": row.student_name,
            "father_name": row.father_name,
            "department_name": row.department_name,
            "course_name": row.name,
            "paid": row.paid,
            "discount": row.discount,
            "date": row.date.strftime("%Y-%m-%d")
        })

    #   -- write csv --
    df = pd.DataFrame(data)
    if df.shape[0] > 0:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df["date"] = df["date"].apply(
        lambda x: f"{x.year}-{x.strftime('%b').lower()}-{x.day}")

    return df


def generate_income_data(
    session_id,
    month_id, 
    day_id, 
    db
    ):

    query = (
        db.query(
            InstituteIncome.income_id, 
            InstituteIncome.income_type,
            InstituteIncome.income_details,
            InstituteIncome.income_from,
            InstituteIncome.amount,
            InstituteIncome.date
        )
    )

    # -- apply filters dynamically --
    if session_id:
        query = query.filter(extract("year", InstituteIncome.date) == int("20"+session_id))
    if month_id and month_id.isdigit():
        query = query.filter(extract("month", InstituteIncome.date) == int(month_id))
    if day_id and day_id.isdigit():
        query = query.filter(extract("day", InstituteIncome.date) == int(day_id))

    # -- execute query --
    results = query.order_by(InstituteIncome.date).all()

    # -- jesonify response --
    data = []
    for row in results:
        data.append(
            {
                "income_id": row.income_id, 
                "income_details": row.income_details,
                "income_from": row.income_from, 
                "amount": row.amount,
                "date": row.date.strftime("%Y-%m-%d")
            }
        )

    #   -- write csv --
    df = pd.DataFrame(data)
    if df.shape[0] > 0:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df["date"] = df["date"].apply(
        lambda x: f"{x.year}-{x.strftime('%b').lower()}-{x.day}")

    # -- return --
    return df


@reports_router.post("/salary_report")
async def salary_report(
    request: Request,
    db: Session = Depends(get_db)
    ):

    # -- get form data --
    form_data = await request.form()
    session_id = form_data.get("session_id")
    month_id = form_data.get("month_id")
    day_id = form_data.get("day_id")

    # -- generate salary data --
    df = generate_salary_data(
        session_id,
        month_id,
        day_id,
        db
    )

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer,
        media_type = "text/csv",
        headers = {
            "Content-Disposition": f"attachment; filename=salary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@reports_router.post("/institute_expense_report")
async def institute_expense_report(
    request: Request,
    db: Session = Depends(get_db)
    ):

    # -- get form data --
    form_data = await request.form()
    session_id = form_data.get("session_id")
    month_id = form_data.get("month_id")
    day_id = form_data.get("day_id")

    # -- expense daata -- 
    df = generate_expense_data(
        session_id,
        month_id,
        day_id,
        db
    )

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer,
        media_type = "text/csv",
        headers = {
            "Content-Disposition": f"attachment; filename=institute_expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@reports_router.post("/fee_report")
async def fee_report(
    request: Request,
    db: Session = Depends(get_db)
):
    # -- get form data --
    form_data = await request.form()
    session_id = form_data.get("session_id")
    month_id = form_data.get("month_id")
    day_id = form_data.get("day_id")

    # -- expense daata -- 
    df = generate_fee_data(
        session_id,
        month_id,
        day_id,
        db
    )

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer,
        media_type = "text/csv",
        headers = {
            "Content-Disposition": f"attachment; filename=fee_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@reports_router.post("/institute_income_report")
async def institute_income_report(
    request: Request,
    db: Session = Depends(get_db)
):
        # -- get form data --
    form_data = await request.form()
    session_id = form_data.get("session_id")
    month_id = form_data.get("month_id")
    day_id = form_data.get("day_id")

    # -- generate extra income; if --
    df = generate_income_data(
        session_id, 
        month_id, 
        day_id, 
        db
    )

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer,
        media_type = "text/csv",
        headers = {
            "Content-Disposition": f"attachment; filename=institute_income_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )



@reports_router.post("/report_01_income_statement")
async def report_01_income_statement(
    request: Request,
    db: Session = Depends(get_db)
):
    # -- get form data --
    form_data = await request.form()
    session_id = form_data.get("session_id")
    month_id = form_data.get("month_id")
    day_id = form_data.get("day_id")


    # ===== INCOME REPORTS =====
    # -- generate salary data --
    salary_data = generate_salary_data(
        session_id,
        month_id,
        day_id,
        db
    )
    # -- expense daata -- 
    expense_data = generate_expense_data(
        session_id,
        month_id,
        day_id,
        db
    )
    # print(salary_data)
    # print(expense_data)

    # ===== EXPENSES REPORTS =====
    # -- generate fee data --
    fee_data = generate_fee_data(
        session_id,
        month_id,
        day_id,
        db
    )
    # -- generate extra income; if --
    income_data = generate_income_data(
        session_id, 
        month_id, 
        day_id, 
        db
    )
    # print(fee_data)
    # print(income_data)
    
    # -- write to excel --
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        income_data.to_excel(writer, sheet_name="Institute_Income", index=False)
        fee_data.to_excel(writer, sheet_name="Student_Fee", index=False)
        expense_data.to_excel(writer, sheet_name="Institute_Expenses", index=False)
        salary_data.to_excel(writer, sheet_name="Institute_Salary", index=False)
    buffer.seek(0)

    # -- return as response --
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
    )



@reports_router.get("/student_mini_form", response_class=HTMLResponse)
async def student_mini_form(
    request: Request
    ):

    return templates.TemplateResponse(
        "pages/reports/student_mini_form.html",
        {
            "request": request
        }
    )
    

@reports_router.get("/student_mini_report/{student_id}", response_class=HTMLResponse)
async def student_mini_report(
    request: Request,
    student_id: int,
    db: Session = Depends(get_db)
):

    # -- 1. Fetch Student --
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # -- 2. Fetch Enrollments --
    enrollments = (
        db.query(StudentEnrollment, Department, Course, 
                Shift, ClassCode, AdmissionType, Semester
                )
        .join(Department, StudentEnrollment.department_id == Department.department_id)
        .join(Course, StudentEnrollment.course_id == Course.course_id)
        .join(Shift, StudentEnrollment.shift_id == Shift.shift_id)
        .join(ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id)
        .join(AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id)
        .join(Semester, StudentEnrollment.semester_id == Semester.semester_id)
        .filter(StudentEnrollment.student_id == student_id)
        .order_by(StudentEnrollment.student_id.asc())
        .all()
    )

    # -- 3. Build Enrollment Data with Nested Fees --
    enrollment_list = []
    for en, dep, course, shift, class_code, admission_type, semester in enrollments:
        
        # Fetch fees for THIS specific enrollment
        fee_info = util_fee_extract(
            en.student_id, en.department_id, 
            en.course_id, en.shift_id, en.class_code_id, 
            en.admission_type_id, en.semester_id, db
        )

        enrollment_list.append({
            "course_name": course.name,
            "status": "Active",  # You can make this dynamic if you have a status column
            "department": dep.department_name,  # HTML expects 'department'
            "class_code": class_code.class_code_name,
            "shift": shift.shift_name,
            "semester": semester.semester,
            # "admission_date": en.date, # Assuming StudentEnrollment has a date column
            "total_fee": en.fee,
            "fees": fee_info  # <--- CRITICAL: Nesting the fees here
        })

    # -- 4. Build Student Data (Matching HTML keys) --
    student_data = {
        "id": student.student_id,
        "name": student.name,
        "father_name": student.father_name,
        "dob": student.date_of_birth.strftime("%Y-%m-%d") if student.date_of_birth else "N/A", # HTML expects 'dob'
        "cnic": student.cnic,
        "nationality": student.nationality,
        "gender": student.gender,
        "mobile": student.mobile, # HTML expects 'mobile'
        "emergency_contact": student.emergency,
        "temp_address": student.temporary_address,
        "perm_address": student.permanent_address, # HTML expects 'perm_address'
    }


    return templates.TemplateResponse(
        "pages/reports/student_mini_report.html",
        {
            "request": request,
            "student": student_data,
            "enrollments_list": enrollment_list # We pass this as a standalone list
        }
    )



def util_fee_extract(
    student_id: int = None,
    department_id: int = None, 
    course_id: int = None, 
    shift_id: int = None,
    class_code_id: int = None,
    admission_type_id: int = None,
    semester_id: int = None,
    db = None
    ):

    # -- extract filters --
    result = (
        db.query(StudentFee, PaymentType)
        .join(
            PaymentType,
            PaymentType.payment_type_id == StudentFee.fee_type_id
        )
        .filter(
            and_(
                StudentFee.student_id == student_id if student_id else True,
                StudentFee.department_id == department_id if department_id else True,
                StudentFee.course_id == course_id if course_id else True,
                StudentFee.shift_id == shift_id if shift_id else True,
                StudentFee.class_code_id == class_code_id if class_code_id else True,
                StudentFee.admission_type_id == admission_type_id if admission_type_id else True,
                StudentFee.semester_id == semester_id if semester_id else True
            )
        )
        .order_by(StudentFee.payment_id.asc())
        .all()
    )
    
    # FIX: Check if result exists first
    if result:
        # FIX: Unpack the result or access via Class Name
        # result[0] is StudentFee, result[1] is PaymentType
        data = []
        for student_fee_obj, payment_type_obj in result:
            data.append({
                "fee_type": payment_type_obj.payment_type_name, # Access name from PaymentType entity
                "paid_amount": student_fee_obj.paid,       # Access amount from StudentFee entity
                "discount": student_fee_obj.discount,
                "date": student_fee_obj.date
            })
        return data
    
    # Return default if no fee record found
    return {
        "fee_type": "N/A",
        "paid_amount": 0.0,
        "discount": 0.0,
        "date": None
    }
