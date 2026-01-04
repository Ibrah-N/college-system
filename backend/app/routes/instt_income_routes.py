from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)
import pandas as pd
import io

from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal

from app.models.institute_income_orm import InstituteIncome
from app.models.helper_orm import Shift


income_router = APIRouter(prefix="/account", tags=['Account'])
templates = Jinja2Templates("frontend")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================================
#  L O A D - I N C O M E   - F O R M   #
# ======================================
@income_router.get("/income_form")
def income_form(request: Request):
    return templates.TemplateResponse(
        "pages/instt_income/instt_income.html",
        {"request": request}
    )



# ======================================
#        A D D - I N C O M E           #
# ======================================
@income_router.post("/add_income")
async def add_income(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    print(form_data)
    # -- amount var check --
    amount = 0
    if form_data.get("amount")=='' or form_data.get("amount") is None:
        amount = 0
    else:
        amount = float(form_data.get("amount"))
    new_income = InstituteIncome(
        income_type=form_data.get("income_type"), income_details=form_data.get("income_details"),
        income_from=form_data.get("income_from"), amount=amount,
        shift_id=form_data.get("shift_id"))
    # -- add income --
    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    # -- response --
    return RedirectResponse(
        url="/account/list_incomes",
        status_code=303
    )


# ======================================
#      L I S T - I N C O M E S       #
# ======================================
@income_router.get("/list_incomes")
def list_incomes(request: Request, db: Session = Depends(get_db)):
    all_incomes = db.query(InstituteIncome).all()

    # -- extract all neccessory info --
    result = (
        db.query(InstituteIncome, Shift)
        .join(Shift, InstituteIncome.shift_id == Shift.shift_id)
        .all()
    )

    # -- jsonify record for fastapi responses --
    json_incomes = []
    for instt_inc, sh in result:
        json_incomes.append({
            "id": instt_inc.income_id,
            "income_details": instt_inc.income_details,
            "income_type": instt_inc.income_type,
            "income_from": instt_inc.income_from,
            "amount": instt_inc.amount,
            "shift": sh.shift_name,
            "shift_id": sh.shift_id,
            "date": instt_inc.date.isoformat() if instt_inc.date else None
        })

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income/instt_income_table.html",
        {
            "request": request,
            "incomes": json_incomes
        }
    )


# ======================================
#      D E L E T E - I N C O M E.      #
# ======================================
@income_router.delete("/delete_income")
def delete_income(
        id: int, 
        db: Session = Depends(get_db)
    ):
    
    # -- filter income --
    income = db.query(InstituteIncome).filter_by(
        income_id=id
    ).first()

    # -- existance check --
    if not income:
        return JSONResponse(
            content = {
                "message": "Income not found!!"
            }, status_code = 404
        )

    # -- delete ---
    db.delete(income)
    db.commit()

    # -- response --
    return RedirectResponse(
        url="/account/list_incomes",
        status_code=303
    )



# ======================================
#      U P D A T E -  I N C O M E.     #
# ======================================
@income_router.get("/update_income_stage_1/{income_id}")
async def update_expense_stage_1(request: Request, income_id: int,
                                 db: Session = Depends(get_db)):

    # -- joins --
    query = (
        db.query(InstituteIncome, Shift
                )
        .join(Shift, InstituteIncome.shift_id == Shift.shift_id)
    )
    query = query.filter(
        InstituteIncome.income_id==income_id
    )
    result = query.first()


    # -- existance check --
    if not result:
        return JSONResponse(
            content = {
                "message": "Income not found!!"
            }, status_code = 404
        )
    
    # -- jsonify incomes --
    json_income = {
        "id": result.InstituteIncome.income_id,
        "income_type": result.InstituteIncome.income_type,
        "income_details": result.InstituteIncome.income_details,
        "income_from": result.InstituteIncome.income_from,
        "amount": result.InstituteIncome.amount,
        "shift": result.Shift.shift_name,
        "shift_id": result.InstituteIncome.shift_id,   
        "date": result.InstituteIncome.date.isoformat() if result.InstituteIncome.date else None
    }

    # -- fetch shifts for dropdowns --
    shifts = db.query(Shift).all()

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income/update_instt_income.html",
        {
            "request": request,
            "old_income": json_income,
            "shifts": shifts
        }
    )


@income_router.post("/update_income")
async def update_income(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    income_id = form_data.get("income_id")

    # -- filter income --
    income = db.query(InstituteIncome).filter(
        InstituteIncome.income_id == income_id
    ).first()

    # -- existance check --
    if not income:
        return JSONResponse(
            content = {
                "message": "Income not found!!"
            }, status_code = 404
        )

    # -- update expense --
    income.income_type = form_data.get("income_type")
    income.income_details = form_data.get("income_details")
    income.income_from = form_data.get("income_from")
    income.amount = float(form_data.get("amount")) if form_data.get("amount") else 0
    income.shift_id = form_data.get("shift_id")

    db.commit()

    # -- response --
    return RedirectResponse(
        url="/account/list_incomes",
        status_code=303
    )


# ======================================
#      S E A R C H - I N C O M E S.    #
# ======================================
@income_router.post("/search_incomes")
async def search_incomes(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    # -- extract join data --
    query = (
        db.query(InstituteIncome, Shift
                )
        .join(Shift, InstituteIncome.shift_id == Shift.shift_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            InstituteIncome.income_id==int(form_data.get("id_search"))
        )
        result = query.all()

        # -- jsonify --
        json_expenses = []
        for instt_inc, sh in result:
            json_expenses.append({
                "id": instt_inc.income_id,
                "income_type": instt_inc.income_type,
                "income_details": instt_inc.income_details,
                "income_from": instt_inc.income_from,
                "amount": instt_inc.amount,
                "shift": sh.shift_name,
                "shift_id": sh.shift_id,
                "date": instt_inc.date.isoformat() if instt_inc.date else None
            })

        # -- response --
        return templates.TemplateResponse(
            "pages/instt_income/instt_income_table.html",
            {
                "request": request,
                "expenses": json_expenses
            }
        )

    # -- by search income type --
    if form_data.get("income_type"):
        query = query.filter(
            InstituteIncome.income_type.ilike(f"%{form_data.get("income_type")}%")
        )
    # -- income details search --
    if form_data.get("income_from"):
        query = query.filter(
            InstituteIncome.income_from.ilike(f"%{form_data.get("income_from")}%")
        )
    # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            InstituteIncome.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    json_expenses = []
    for instt_inc, sh in result:
        json_expenses.append({
            "id": instt_inc.income_id,
            "income_type": instt_inc.income_type,
            "income_details": instt_inc.income_details,
            "income_from": instt_inc.income_from,
            "amount": instt_inc.amount,
            "shift": sh.shift_name,
            "shift_id": sh.shift_id,
            "date": instt_inc.date.isoformat() if instt_inc.date else None
        })

    # -- response --
    return templates.TemplateResponse(
        "pages/instt_income/instt_income_table.html",
        {
            "request": request,
            "incomes": json_expenses
        }
    )


# ======================================
#      E X P O R T - I N C O M E       #
# ======================================
@income_router.post("/export_incomes")
async def export_incomes(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    # -- extract join data --
    query = (
        db.query(InstituteIncome, Shift
                )
        .join(Shift, InstituteIncome.shift_id == Shift.shift_id)
    )

    # -- search by id --
    if form_data.get("id_search"):
        query = query.filter(
            InstituteIncome.income_id==int(form_data.get("id_search"))
        )
        result = query.all()

        # -- jsonify --
        json_expenses = []
        for instt_inc, sh in result:
            json_expenses.append({
                "id": instt_inc.income_id,
                "income_type": instt_inc.income_type,
                "income_details": instt_inc.income_details,
                "income_from": instt_inc.income_from,
                "shift": sh.shift_name,
                "amount": instt_inc.amount,
                "date": instt_inc.date.isoformat() if instt_inc.date else None,
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
                "Content-Disposition": "attachment; filename=exported_incomes.csv"
            }
        )


    # -- expense by search --
    if form_data.get("income_type"):
        query = query.filter(
            InstituteIncome.income_type.ilike(f"%{form_data.get("income_type")}%")
        )
    # -- item detail search --
    if form_data.get("income_from"):
        query = query.filter(
            InstituteIncome.income_from.ilike(f"%{form_data.get("income_from")}%")
        )

    # # -- shift search --
    if form_data.get("shift_id"):
        query = query.filter(
            InstituteIncome.shift_id==int(form_data.get("shift_id"))
        )
    result = query.all()

    # -- jsonify --
    json_expenses = []
    for instt_inc, sh in result:
        json_expenses.append({
            "id": instt_inc.income_id,
            "income_type": instt_inc.income_type,
            "income_details": instt_inc.income_details,
            "income_from": instt_inc.income_from,
            "shift": sh.shift_name,
            "amount": instt_inc.amount,
            "date": instt_inc.date.isoformat() if instt_inc.date else None,
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
            "Content-Disposition": "attachment; filename=exported_incomes.csv"
        }
    )
