from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import Query


from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.admission_orm import Student


from app.utils.form_submission import (title_case, 
                                        validate_cnic, 
                                        validate_phone_number
                                    )


admission_router = APIRouter(prefix="/student", tags=["Student"])
templates = Jinja2Templates(directory="frontend")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# ========================================
#  S T U D E N T S - M A I N - F O R M   #
# ========================================
# @admission_router.get("/", response_class=HTMLResponse)
# def student(request: Request):
#     return templates.TemplateResponse("pages/main/student.html", {"request":request})



# ========================================
#  L O A D - S T U D E N T S - F O R M   #
# ========================================
@admission_router.get("/admission", response_class=HTMLResponse)
def get_students(request: Request):
    return templates.TemplateResponse("pages/student/admission_form.html", {"request":request})



# ========================================
#       R E A D  -  S T U D E N T S      #
# ========================================
@admission_router.get("/all")
def get_all_students(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.student_id.asc()).all()
    
    return templates.TemplateResponse("pages/student/admission_table.html", 
                                        {"request": request, "students": students})



# ========================================
#       A D D  -  S T U D E N T          #
# ========================================
@admission_router.post("/add")
async def add_student(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    

    # -- check whether have unset values --
    emergency_no = validate_phone_number(form_data.get("emergency_no")) or ""
    degree = form_data.get("degree") or ""
    name_of_institute = form_data.get("name_of_institute") or ""
    academic_year = form_data.get("academic-year") or ""
    grade = form_data.get("grade") or ""

    # -- add new student --
    new_student = Student(
        name=title_case(form_data.get("student_name")), 
        father_name=title_case(form_data.get("father_name")),
        gender=form_data.get("gender"), 
        date_of_birth=form_data.get("date_of_birth"),
        nationality=title_case(form_data.get("nationality")), 
        cnic=validate_cnic(form_data.get("cnic")) or "",
        mobile=validate_phone_number(form_data.get("mobile")) or "", 
        emergency=validate_phone_number(emergency_no), 
        temporary_address=title_case(form_data.get("temp_address")) or "", 
        permanent_address=title_case(form_data.get("perm_address")) or "",
        degree=degree, 
        year=academic_year,
        name_of_institute=title_case(name_of_institute) or "", 
        grade=grade
        )


    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return RedirectResponse(url="/student/all", status_code=303)



# ========================================
#      U P D A T E -  S T U D E N T      #
# ========================================
@admission_router.get("/update_stage_1/{student_id}", response_class=HTMLResponse)
async def update_stage_1_student(request: Request, student_id: int, db: Session = Depends(get_db)):
    student_old = db.query(Student).filter(Student.student_id == student_id).first()

    if not student_old:
        return JSONResponse(content={"message": f"Student with ID {studnet_id} not found !!!"}, status_code=404)

    # -- load the data to update form --
    return templates.TemplateResponse(
        "pages/student/update_student.html",
        {"request": request, "old_student": student_old})


@admission_router.post("/update_student")
async def update_student(request: Request, db: Session = Depends(get_db)):
    
    # -- recieve form data --
    form_data = await request.form()
    student_id = int(form_data.get("student_id"))

    # -- find existing student --
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return JSONResponse(content={"message": "Student not found"}, status_code=404)

    # -- check whether have unset values --
    emergency_no = form_data.get("emergency_no") or ""
    degree = form_data.get("degree") or ""
    name_of_institute = form_data.get("name_of_institute") or ""
    academic_year = form_data.get("academic-year") or ""
    grade = form_data.get("grade") or ""

    # -- update student --
    student.name = title_case(form_data.get("student_name"))
    student.father_name = title_case(form_data.get("father_name"))
    student.gender = form_data.get("gender")
    student.date_of_birth = form_data.get("date_of_birth")
    student.nationality = title_case(form_data.get("nationality"))
    student.cnic = validate_cnic(form_data.get("cnic"))
    student.mobile = validate_phone_number(form_data.get("mobile"))
    student.temporary_address = title_case(form_data.get("temp_address"))
    student.permanent_address = title_case(form_data.get("perm_address"))
    student.emergency = validate_phone_number(emergency_no)
    student.degree = degree
    student.year = academic_year
    student.name_of_institute = title_case(name_of_institute)
    student.grade = grade

    db.commit()
    return RedirectResponse(url="/student/all", status_code=303)





# ========================================
#    D E L E T E  -  S T U D E N T       #
# ========================================
@admission_router.delete("/delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()

    if not student:
        return JSONResponse(content = {"message": "Student not found"}, status_code=404)

    db.delete(student)
    db.commit()

    return JSONResponse(content = {"message" : "Student Delete successfully"}, status_code=200)




# ========================================
#     S E A R C H -  S T U D E N T       #
# ========================================
@admission_router.get("/search_student")
async def search_student(request: Request, id_search,
                name_search, db: Session = Depends(get_db)
            ):

    students = db.query(Student).order_by(Student.student_id.asc()).all()
    if id_search:
        students = db.query(Student).filter(Student.student_id == id_search).order_by(Student.student_id.asc()).first()
    elif name_search:
        students = db.query(Student).filter(Student.name.ilike(f"%{name_search}%")).order_by(Student.student_id.asc()).all()

    if isinstance(students, Student):
        students = [students]
    
    if not students:
        students = []

    return templates.TemplateResponse(
        "pages/student/admission_table.html", 
        {"request": request, "students": students}
    )



@admission_router.post("/check_student")
async def check_student(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    student_id = data.get("student_id")

    exists = db.query(Student).filter(Student.student_id == student_id).first()

    return {
        "exists": True if exists else False
    }
