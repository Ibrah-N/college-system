from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.add_teacher_orm import AddTeacher


# -- add paths --
add_teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])
templates = Jinja2Templates(directory="frontend")

# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ========================================
#  T E A C H E R - M A I N - F O R M   #
# ========================================
@add_teacher_router.get("/", response_class=HTMLResponse)
def teacher(request: Request):
    return templates.TemplateResponse("pages/main/teacher.html", {"request": request})



# ========================================
#  L O A D - T E A C H E R - F O R M    #
# ========================================
@add_teacher_router.get("/add_teacher", response_class=HTMLResponse)
def get_teacher(request: Request):
    return templates.TemplateResponse("pages/teacher/add_teacher.html", {"request": request})


# ========================================
#       R E A D  -  T E A C H E R       #
# ========================================
@add_teacher_router.get("/all", response_class=HTMLResponse)
def get_all_teacher(request: Request):
    pass


# ========================================
#       A D D  -  T E A C H E R          #
# ========================================



# ========================================
#      U P D A T E -  T E A C H E R      #
# ========================================



# ========================================
#    D E L E T E  -  T E A C H E R       #
# ========================================



# ========================================
#     S E A R C H -  T E A C H E R       #
# ========================================



