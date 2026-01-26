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