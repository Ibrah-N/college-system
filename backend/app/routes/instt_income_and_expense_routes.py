from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)
import pandas as pd
import io

from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal

from app.models.institute_expense_orm import InstituteExpense
from app.models.helper_orm import (Session, Month, Day, Shift)


income_expense_router = APIRouter(prefix="/account", tags=['Account'])
templates = Jinja2Templates("frontend")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ======================================
#  L O A D - E X P E N S E - F O R M   #
# ======================================
@income_expense_router.get("/expense_form")
def expense_form(request: Request):
    return templates.TemplateResponse(
        "pages/instt_income_and_expense/instt_expense.html",
        {"request": request}
    )


# ======================================
#        A D D - E X P E N S E         #
# ======================================
@income_expense_router.post("/add_expense")
async def add_expense(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    print(form_data)
    # -- amount var check --
    amount = 0
    if form_data.get("amount")=='' or form_data.get("amount") is None:
        amount = 0
    else:
        amount = float(form_data.get("amount"))
    new_expense = InstituteExpense(
        item_detail=form_data.get("item_details"), expense_for=form_data.get("expense_for"),
        expense_by=form_data.get("expense_by"), amount=amount,
        session_id=form_data.get("session_id"), month_id=form_data.get("month_id"),
        day_id=form_data.get("day_id"), shift_id=form_data.get("shift_id"))
    
    # -- add expense --
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    # -- response --
    return RedirectResponse(
        url="/account/list_expenses",
        status_code=303
    )


# ======================================
#      L I S T - E X P E N S E S       #
# ======================================
@income_expense_router.get("/list_expenses")
def list_expenses(request: Request, db: Session = Depends(get_db)):
    all_expenses = db.query(InstituteExpense).all()

    # -- extract all neccessory info --
    result = (
        db.query(InstituteExpense, Session,
                 Month, Day, Shift
                )
        .join(Session, InstituteExpense.session_id == Session.session_id)
        .join(Month, InstituteExpense.month_id == Month.month_id)
        .join(Day, InstituteExpense.day_id == Day.day_id)
        .join(Shift, InstituteExpense.shift_id == Shift.shift_id)
        .all()
    )

    # -- jsonify record for fastapi responses --
    json_expenses = []
    for instt_exp, s, m, d, sh in result:
        json_expenses.append({
            "id": instt_exp.expense_id,
            "item_detail": instt_exp.item_detail,
            "expense_for": instt_exp.expense_for,
            "expense_by": instt_exp.expense_by,
            "amount": instt_exp.amount,
            "session": s.session,
            "session_id": s.session_id,
            "month": m.month,
            "month_id": m.month_id,
            "day": d.day,
            "day_id": d.day_id,
            "shift": sh.shift_name,
            "shift_id": sh.shift_id,
            "date": instt_exp.date.isoformat() if instt_exp.date else None
        })

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income_and_expense/instt_expense_table.html",
        {
            "request": request,
            "expenses": json_expenses
        }
    )


# ======================================
#      D E L E T E - E X P E N S E S   #
# ======================================
@income_expense_router.delete("/delete_expense")
def delete_expense(
        id: int, session_id: int, 
        month_id: int, day_id:int, 
        db: Session = Depends(get_db)
    ):
    
    # -- filter expense --
    expense = db.query(InstituteExpense).filter_by(
        expense_id=id, 
        session_id=session_id, 
        month_id=month_id, 
        day_id=day_id
    ).first()

    # -- existance check --
    if not expense:
        return JSONResponse(
            content = {
                "message": "Expense not found!!"
            }, status_code = 404
        )

    # -- delete ---
    db.delete(expense)
    db.commit()

    # -- response --
    return RedirectResponse(
        url="/account/list_expenses",
        status_code=303
    )



# ======================================
#      U P D A T E - E X P E N S E S   #
# ======================================
@income_expense_router.get("/update_expense_stage_1/{expense_id}")
async def update_expense_stage_1(request: Request, expense_id: int,
                                 db: Session = Depends(get_db)):

    # -- joins --
    query = (
        db.query(InstituteExpense, Session,
                 Month, Day, Shift
                )
        .join(Session, InstituteExpense.session_id == Session.session_id)
        .join(Month, InstituteExpense.month_id == Month.month_id)
        .join(Day, InstituteExpense.day_id == Day.day_id)
        .join(Shift, InstituteExpense.shift_id == Shift.shift_id)
    )
    query = query.filter(
        InstituteExpense.expense_id==expense_id
    )
    result = query.first()


    # -- existance check --
    if not result:
        return JSONResponse(
            content = {
                "message": "Expense not found!!"
            }, status_code = 404
        )
    
    # -- jsonify expense --
    json_expense = {
        "id": result.InstituteExpense.expense_id,
        "item_detail": result.InstituteExpense.item_detail,
        "expense_for": result.InstituteExpense.expense_for,
        "expense_by": result.InstituteExpense.expense_by,
        "amount": result.InstituteExpense.amount,
        "session": result.Session.session,
        "session_id": result.InstituteExpense.session_id,
        "month": result.Month.month,
        "month_id": result.InstituteExpense.month_id,
        "day": result.Day.day, 
        "day_id": result.InstituteExpense.day_id,
        "shift": result.Shift.shift_name,
        "shift_id": result.InstituteExpense.shift_id,   
        "date": result.InstituteExpense.date.isoformat() if result.InstituteExpense.date else None
    }

    # -- fetch sessions, months, days, shifts for dropdowns --
    sessions = db.query(Session).all()
    months = db.query(Month).all()
    days = db.query(Day).all()
    shifts = db.query(Shift).all()

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income_and_expense/update_instt_expense.html",
        {
            "request": request,
            "old_expense": json_expense,
            "sessions": sessions,
            "months": months,
            "days": days,
            "shifts": shifts
        }
    )


@income_expense_router.post("/update_expense")
async def update_expense(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    expense_id = form_data.get("expense_id")

    # -- filter expense --
    expense = db.query(InstituteExpense).filter(
        InstituteExpense.expense_id == expense_id
    ).first()

    # -- existance check --
    if not expense:
        return JSONResponse(
            content = {
                "message": "Expense not found!!"
            }, status_code = 404
        )

    # -- update expense --
    expense.item_detail = form_data.get("item_details")
    expense.expense_for = form_data.get("expense_for")
    expense.expense_by = form_data.get("expense_by")
    expense.amount = float(form_data.get("amount")) if form_data.get("amount") else 0
    expense.session_id = form_data.get("session_id")
    expense.month_id = form_data.get("month_id")
    expense.day_id = form_data.get("day_id")
    expense.shift_id = form_data.get("shift_id")

    db.commit()

    # -- response --
    return RedirectResponse(
        url="/account/list_expenses",
        status_code=303
    )






# ======================================
#      S E A R C H - E X P E N S E S   #
# ======================================
@income_expense_router.post("/search_expense")
async def search_expense(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    # -- extract join data --
    query = (
        db.query(InstituteExpense, Session,
                 Month, Day, Shift
                )
        .join(Session, InstituteExpense.session_id == Session.session_id)
        .join(Month, InstituteExpense.month_id == Month.month_id)
        .join(Day, InstituteExpense.day_id == Day.day_id)
        .join(Shift, InstituteExpense.shift_id == Shift.shift_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            InstituteExpense.expense_id==int(form_data.get("id_search"))
        )
        result = query.all()

        # -- jsonify --
        json_expenses = []
        for instt_exp, s, m, d, sh in result:
            json_expenses.append({
                "id": instt_exp.expense_id,
                "item_detail": instt_exp.item_detail,
                "expense_for": instt_exp.expense_for,
                "expense_by": instt_exp.expense_by,
                "amount": instt_exp.amount,
                "session": s.session,
                "session_id": s.session_id,
                "month": m.month,
                "month_id": m.month_id,
                "day": d.day,
                "day_id": d.day_id,
                "shift": sh.shift_name,
                "shift_id": sh.shift_id,
                "date": instt_exp.date.isoformat() if instt_exp.date else None
            })

        # -- response --
        return templates.TemplateResponse(
            "pages/instt_income_and_expense/instt_expense_table.html",
            {
                "request": request,
                "expenses": json_expenses
            }
        )

    # -- expense by search --
    if form_data.get("expense_by"):
        query = query.filter(
            InstituteExpense.expense_by.ilike(f"%{form_data.get("expense_by")}%")
        )
    # -- item detail search --
    if form_data.get("item_detail"):
        query = query.filter(
            InstituteExpense.item_detail.ilike(f"%{form_data.get("item_detail")}%")
        )
    # -- session search --
    if form_data.get("session_id"):
        query = query.filter(
            InstituteExpense.session_id==int(form_data.get("session_id"))
        )
    # -- month search --
    if form_data.get("month_id"):
        query = query.filter(
            InstituteExpense.month_id==int(form_data.get('month_id'))
        )
    # -- day search --
    if form_data.get("day_id"):
        query = query.filter(
            InstituteExpense.day_id==int(form_data.get("day_id"))
        )
    # # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            InstituteExpense.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    json_expenses = []
    for instt_exp, s, m, d, sh in result:
        json_expenses.append({
            "id": instt_exp.expense_id,
            "item_detail": instt_exp.item_detail,
            "expense_for": instt_exp.expense_for,
            "expense_by": instt_exp.expense_by,
            "amount": instt_exp.amount,
            "session": s.session,
            "session_id": s.session_id,
            "month": m.month,
            "month_id": m.month_id,
            "day": d.day,
            "day_id": d.day_id,
            "shift": sh.shift_name,
            "shift_id": sh.shift_id,
            "date": instt_exp.date.isoformat() if instt_exp.date else None
        })

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income_and_expense/instt_expense_table.html",
        {
            "request": request,
            "expenses": json_expenses
        }
    )


# ======================================
#      E X P O R T - E X P E N S E S   #
# ======================================
@income_expense_router.post("/export_expenses")
async def export_expense(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    # -- extract join data --
    query = (
        db.query(InstituteExpense, Session,
                    Month, Day, Shift
                )
        .join(Session, InstituteExpense.session_id == Session.session_id)
        .join(Month, InstituteExpense.month_id == Month.month_id)
        .join(Day, InstituteExpense.day_id == Day.day_id)
        .join(Shift, InstituteExpense.shift_id == Shift.shift_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            InstituteExpense.expense_id==int(form_data.get("id_search"))
        )
        result = query.all()

        # -- jsonify --
        json_expenses = []
        for instt_exp, s, m, d, sh in result:
            json_expenses.append({
                "id": instt_exp.expense_id,
                "item_detail": instt_exp.item_detail,
                "expense_for": instt_exp.expense_for,
                "expense_by": instt_exp.expense_by,
                "shift": sh.shift_name,
                "amount": instt_exp.amount,
                "date": instt_exp.date.isoformat() if instt_exp.date else None,
                "session": s.session,
                "month": m.month,
                "day": d.day
            })

        # -- write csv --
        df = pd.DataFrame(json_expenses)

        # -- export csv --
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        # -- response --
        return StreamingResponse(
            buffer,
            media_type = "text/csv",
            headers = {
                "Content-Disposition": "attachment; filename=exported_expenses.csv"
            }
        )


    # -- expense by search --
    if form_data.get("expense_by"):
        query = query.filter(
            InstituteExpense.expense_by.ilike(f"%{form_data.get("expense_by")}%")
        )
    # -- item detail search --
    if form_data.get("item_detail"):
        query = query.filter(
            InstituteExpense.item_detail.ilike(f"%{form_data.get("item_detail")}%")
        )
    # -- session search --
    if form_data.get("session_id"):
        query = query.filter(
            InstituteExpense.session_id==int(form_data.get("session_id"))
        )
    # -- month search --
    if form_data.get("month_id"):
        query = query.filter(
            InstituteExpense.month_id==int(form_data.get('month_id'))
        )
    # -- day search --
    if form_data.get("day_id"):
        query = query.filter(
            InstituteExpense.day_id==int(form_data.get("day_id"))
        )
    # # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            InstituteExpense.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    json_expenses = []
    for instt_exp, s, m, d, sh in result:
        json_expenses.append({
            "id": instt_exp.expense_id,
            "item_detail": instt_exp.item_detail,
            "expense_for": instt_exp.expense_for,
            "expense_by": instt_exp.expense_by,
            "shift": sh.shift_name,
            "amount": instt_exp.amount,
            "date": instt_exp.date.isoformat() if instt_exp.date else None,
            "session": s.session,
            "month": m.month,
            "day": d.day
        })

    # -- response --
    df = pd.DataFrame(json_expenses)

    # -- export csv --
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # -- response --
    return StreamingResponse(
        buffer,
        media_type = "text/csv",
        headers = {
            "Content-Disposition": "attachment; filename=exported_expenses.csv"
        }
    )





