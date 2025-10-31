from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse




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



# ========================================
#  L O A D - S T U D E N T S - F O R M   #
# ========================================
@student_router.get("/", response_class=HTMLResponse)
def get_students(request: Request):
    return templates.TemplateResponse("pages/admission_form.html", {"request":request})



# ========================================
#       R E A D  -  S T U D E N T S      #
# ========================================
@student_router.get("/all")
def get_all_students(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).all()
    
    return templates.TemplateResponse("pages/admission_table.html", {"request": request, "students": students})




# ========================================
#       A D D  -  S T U D E N T          #
# ========================================
@student_router.post("/add")
async def add_student(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    

    # -- check whether have unset values --
    emergency_no = form_data.get("emergency_no") or ""
    degree = form_data.get("degree") or ""
    name_of_institute = form_data.get("name_of_institute") or ""
    academic_year = form_data.get("academic-year") or ""
    grade = form_data.get("grade") or ""



    # -- add new student --
    new_student = Student(
        name=form_data.get("student_name"), father_name=form_data.get("father_name"),
        gender=form_data.get("gender"), date_of_birth=form_data.get("date_of_birth"),
        nationality=form_data.get("nationality"), cnic=form_data.get("cnic"),
        mobile=form_data.get("mobile"), emergency=emergency_no, 
        temporary_address=form_data.get("temp_address"), permanent_address=form_data.get("perm_address"),
        degree=degree, year=academic_year, name_of_institute=name_of_institute, grade=grade)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return JSONResponse(content={"message": "Student added successfully"}, status_code=200)




# ========================================
#      U P D A T E -  S T U D E N T      #
# ========================================
# student_router.post("update_stage_1/{student_id}")
# async def update_stage_1_student():




# ========================================
#    D E L E T E  -  S T U D E N T       #
# ========================================
@student_router.delete("/delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()

    if not student:
        return JSONResponse(content = {"message": "Student not found"}, status_code=404)

    db.delete(student)
    db.commit()

    return JSONResponse(content = {"message" : "Student Delete successfully"}, status_code=200)

