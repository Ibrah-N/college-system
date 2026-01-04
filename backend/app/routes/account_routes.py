from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from sqlalchemy import text



# -- add paths --
account_router = APIRouter(prefix="/account", tags=["Account"])
templates = Jinja2Templates(directory="frontend")

# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
#        A C C O U N T - T A B L E         #
# =========================================
@account_router.get("/account_table", response_class=HTMLResponse)
def get_account_table(request: Request, db: Session = Depends(get_db)):
    query_text = "SELECT * FROM v_account_daily;"
    db_account_data = db.execute(text(query_text)).fetchall()

    
    # -- jsonify data --
    account_table_data = []
    for row in db_account_data:
        account_table_data.append({
            "date": row.account_date,
            "session": row.session,
            "month": row.month,
            "day": row.day,
            "total_fee": row.total_fee,
            "total_salary": row.paid_salary,
            "instt_income": row.instt_income,
            "instt_expense": row.instt_expense,
            "total_income": row.total_income,
            "total_expenses": row.total_expenses,
            "account": row.account
        })

    # print(account_table_data)
    return templates.TemplateResponse(
        "pages/account/account_table.html", 
        {
            "request": request, 
            "account_table_data": account_table_data
        }
    )