from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from sqlalchemy import text



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



@reports_router.get("/report_01")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/reports/report_01_table.html",
        {
            "request": request
        }
    )





