from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# -- routers --
from app.routes.admission_routes import admission_router
from app.routes.add_teacher_routes import add_teacher_router
from app.routes.helper_routes import helper_router
from app.routes.student_enrollment_routes import enrollment_router
from app.routes.teacher_registration_routes import teacher_registration_router
from app.routes.instt_expense_routes import expense_router
from app.routes.instt_income_routes import income_router
from app.routes.student_fee_routes import student_fee_router
from app.routes.teacher_salary_routes import teacher_salary_router
from app.routes.login_routes import login_router


from app.config.db_connect import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


# Mount static directory for CSS, JS, images
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")

# Include the student router
app.include_router(login_router)
app.include_router(admission_router)
app.include_router(add_teacher_router)
app.include_router(helper_router)
app.include_router(enrollment_router)
app.include_router(teacher_registration_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(student_fee_router)
app.include_router(teacher_salary_router)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "pages/main_login/login.html",
        {"request": request}
    )