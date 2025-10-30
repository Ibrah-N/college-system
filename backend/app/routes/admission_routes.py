from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.admission_orm import Student


student_router = APIRouter(prefix="/student", tags=["Student"])
templates = Jinja2Templates(directory="frontend")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@student_router.get("/", response_class=HTMLResponse)
def get_students(request: Request):
    return templates.TemplateResponse("pages/admission_form.html", {"request":request})



@student_router.post("/add")
async def add_student(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    
    return {"message": f"student_name {form_data.get("student_name")}"}
