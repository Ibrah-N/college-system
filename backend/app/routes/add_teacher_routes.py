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
# @add_teacher_router.get("/", response_class=HTMLResponse)
# def teacher(request: Request):
#     return templates.TemplateResponse("pages/main/teacher.html", {"request": request})



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
def get_all_teacher(request: Request, db: Session = Depends(get_db)):
    all_teachers = db.query(AddTeacher).all()

    return templates.TemplateResponse("pages/teacher/add_teacher_table.html", 
                                        {"request": request, "teachers": all_teachers})


# ========================================
#       A D D  -  T E A C H E R          #
# ========================================
@add_teacher_router.post("/add")
async def add_teacher(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    new_teacher = AddTeacher(name=form_data.get("teacher_name"), father_name=form_data.get("father_name"),
        qualification=form_data.get("qualification"), gender=form_data.get("gender"), 
        contact=form_data.get("contact"), address=form_data.get("address")
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return RedirectResponse("/teacher/all", status_code=303)



# ========================================
#      U P D A T E -  T E A C H E R      #
# ========================================
@add_teacher_router.get("/update_stage_1/{teacher_id}", response_class=HTMLResponse)
def update_stage_1(request: Request, teacher_id: int, db: Session = Depends(get_db)):
    old_teacher = db.query(AddTeacher).filter(AddTeacher.teacher_id==teacher_id).first()

    if not old_teacher:
        return JSONResponse(content={"message": "Teacher Not Found"}, status_code=404)

    return templates.TemplateResponse(
        "pages/teacher/update_add_teacher.html",
        {"request": request, "old_teacher": old_teacher}
    )


@add_teacher_router.post("/update_add_teacher")
async def update_add_teacher(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    teacher_id = form_data.get("teacher_id")

    teacher = db.query(AddTeacher).filter(AddTeacher.teacher_id == teacher_id).first()
    if not teacher:
        return JSONResponse(content={"message": "Teacher Not Found"}, status_code=404)

    teacher.name = form_data.get("teacher_name")
    teacher.father_name = form_data.get("father_name")
    teacher.qualification = form_data.get("qualification")
    teacher.gender = form_data.get("gender")
    teacher.contact = form_data.get("contact")
    teacher.address = form_data.get("address")
    db.commit()

    return RedirectResponse(url="/teacher/all", status_code=303)



# ========================================
#    D E L E T E  -  T E A C H E R       #
# ========================================
@add_teacher_router.delete("/delete/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(AddTeacher).filter(AddTeacher.teacher_id==teacher_id).first()

    if not teacher:
        return JSONResponse(content = {"message": "Teacher not found"}, status_code=404)

    db.delete(teacher)
    db.commit()

    return JSONResponse(content = {"message": "Teacher Deleted Successfully"}, status_code=200)




# ========================================
#     S E A R C H -  T E A C H E R       #
# ========================================
@add_teacher_router.get("/search_add_teacher")
def search_add_teacher(request: Request, id_search,
                        name_search, db: Session = Depends(get_db)):

    teachers = None
    if id_search:
        teachers = db.query(AddTeacher).filter(AddTeacher.teacher_id==id_search).first()
        
    elif name_search:
        teachers = db.query(AddTeacher).filter(AddTeacher.name.ilike(f"%{name_search}%")).all()


    if isinstance(teachers, AddTeacher):
        teachers = [teachers]
    
    if not teachers:
        teachers = []

    return templates.TemplateResponse(
        "pages/teacher/add_teacher_table.html", 
        {"request": request, "teachers": teachers}
    )


