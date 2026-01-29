from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from sqlalchemy import text


from sqlalchemy import and_, extract


# from app.models.helper_orm import (TestInfo, SyllabusInfo)


import pandas as pd
import io
from datetime import datetime


# -- add paths --
scholarship_router = APIRouter(prefix="/scholarship", tags=["Scholarship"])
templates = Jinja2Templates(directory="frontend")


# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@scholarship_router.get("/scholarship_form")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/scholarship/scholarship_form.html",
        {
            "request": request
        }
    )

