from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from fastapi.responses import (HTMLResponse, RedirectResponse, 
                                JSONResponse, StreamingResponse,
                                Response
                            )
from fastapi.templating import Jinja2Templates 

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from sqlalchemy import text


from sqlalchemy import and_, extract
from sqlalchemy.orm import defer

from app.models.scholarship_orm import Scholarship 
from app.models.scholarship_utils_orm import (TestInfo, SyllabusInfo)
from app.models.helper_orm import Course

from app.utils.image_processing import read_image
from app.utils.form_submission import (title_case, 
                                        validate_cnic,
                                        validate_phone_number
                                    )

import pandas as pd
import io
from datetime import datetime
from PIL import Image


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


# ============================================================
#              L O A D - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.get("/scholarship_form")
def get_form(request: Request):

    return templates.TemplateResponse(
        "pages/scholarship/scholarship_form.html",
        {
            "request": request
        }
    )



# ============================================================
#              A D D - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.post("/add_scholarship")
async def add_scholarship(
    request: Request,
    # === Form Fields (Must match HTML 'name' attributes) ===
    name: str = Form(...),
    father_name: str = Form(...),
    qualification: str = Form(None),
    whatsapp: str = Form(None),
    current_institute: str = Form(None),
    cnic_formb: str = Form(None),      # Added (was in your HTML)
    address: str = Form(None),         # Added (was in your HTML)
    registration_date: str = Form(None), # Added (was in your HTML)
    course_apply_for: str = Form(None),
    select_test: str = Form(None),
    select_syllabus: str = Form(None), # HTML name is "select_syllabus"
    # === File Upload ===
    photo: UploadFile = File(None),
    # === Database Session ===
    db: Session = Depends(get_db)
    ):

    print("scholarship called")
    # -- if image --
    img = None
    if photo and photo.filename:
        # Read the file bytes
        contents = await photo.read()

        img = read_image(contents)

    # -- save to db --
    new_student = Scholarship(
        name=title_case(name),
        father_name=title_case(father_name),
        qualification=qualification,
        whatsapp=validate_phone_number(whatsapp),
        current_institute=current_institute,
        cnic_formb=validate_cnic(cnic_formb),
        address=title_case(address),
        registration_date=registration_date,
        course_id=course_apply_for,
        photo_blob=img  # <--- Saving the binary image here
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # -- redirect to page--
    return RedirectResponse(
        url="/scholarship/list_scholarship", 
        status_code=303
    )



# ============================================================
#              L I S T - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.get("/list_scholarship")
async def list_scholarship(
    request: Request, 
    db: Session = Depends(get_db)
    ):

    students = (
        db.query(Scholarship, Course)
        .join(
            Course,                            
            Scholarship.course_id == Course.course_id 
        )
        .options(
            defer(Scholarship.photo_blob)  
        )
        .order_by(Scholarship.id)
        .all()
    )

    # -- Result is a list of tuples -- 
    data = []
    for sc, c in students:
        data.append({
            "id" : sc.id,
            "name": sc.name, 
            "father_name": sc.father_name, 
            "qualification": sc.qualification, 
            "whatsapp": sc.whatsapp, 
            "current_institute": sc.current_institute,
            "cnic_formb": sc.cnic_formb, 
            "address": sc.address, 
            "registration_date": sc.registration_date,
            "course": c.name
        })


    # -- response --
    return templates.TemplateResponse(
        "pages/scholarship/scholarship_table.html", 
        {
            "request": request,
            "students": data
        }
    )



# ============================================================
#          U P D A T E - S C H O L A R S H I P               #
# ============================================================



# ============================================================
#          D E L E T E - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.delete("/delete/{id}")
async def delete_scholarship(
    id: int, 
    db: Session = Depends(get_db)
    ):
    scholarship = db.query(Scholarship).filter(Scholarship.id == id).first()
    if scholarship:
        db.delete(scholarship)
        db.commit()
        return RedirectResponse(
            url="/scholarship/list_scholarship",
            status_code=303
        )
    return JSONResponse(
        content={
                "message": "Student not found."
                }, status_code=404
            )



# ============================================================
#          E X P O R T - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.post("/export")
async def export_scholarship(
    request: Request,
    db: Session = Depends(get_db)
    ):

    # -- form data --
    form_data = await request.form()
    id_search = form_data.get("id_search")
    name_search = form_data.get("name_search")
    course_id = form_data.get("course_id")

    # -- fetch filtered scholarship data --
    data = get_data(
        id = id_search if id_search else None,
        name = name_search if name_search else None,
        course_id = course_id if course_id else None,
        db_ = db
    )

    # -- write csv --
    df = pd.DataFrame(data)

    # # --- Export as Excel ---
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scholarship_export.csv"}
    )



# ============================================================
#          S E A R C H - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.post("/search", response_class=HTMLResponse)
async def search_scholarship(
    request: Request,
    db: Session = Depends(get_db)
):
    # -- form data --
    form_data = await request.form()
    id_search = form_data.get("id_search")
    name_search = form_data.get("name_search")
    course_id = form_data.get("course_id")

    # -- fetch filtered scholarship data --
    data = get_data(
        id = id_search if id_search else None,
        name = name_search if name_search else None,
        course_id = course_id if course_id else None,
        db_ = db
    )

    # -- render template --
    return templates.TemplateResponse(
        "pages/scholarship/scholarship_table.html", 
        {
            "request": request,
            "students": data
        }
    )



# ============================================================
#            U T I L S - S C H O L A R S H I P               #
# ============================================================
@scholarship_router.get("/image/{student_id}")
def get_student_image(
    student_id: int, 
    db: Session = Depends(get_db)
    ):
    # 1. Find the student
    student = db.query(Scholarship).filter(Scholarship.id == student_id).first()

    # 2. Check if student exists and has a photo
    if not student or not student.photo_blob:
        # Return a default placeholder image or 404
        # For now, let's just return 404 Not Found
        raise HTTPException(status_code=404, detail="Image not found")

    # 3. Return the binary data directly as an image response
    return Response(content=student.photo_blob, media_type="image/jpeg")



def get_data(id: int= None, 
            name: str = None, 
            course_id: int = None,
            db_ =  None
    ):

    # -- build query --
    query = (
        db_.query(Scholarship, Course)
        .join(
            Course,                            
            Scholarship.course_id == Course.course_id 
        )
        .options(
            defer(Scholarship.photo_blob)  
        )
    )

    if id is not None:
        query = query.filter(
            Scholarship.id == id
        )
        results = query.order_by(Scholarship.id).all()

        # -- jesonfiy --
        data = []
        for sc, c in results:
            data.append({
                "id" : sc.id,
                "name": sc.name, 
                "father_name": sc.father_name, 
                "qualification": sc.qualification, 
                "whatsapp": sc.whatsapp, 
                "current_institute": sc.current_institute,
                "cnic_formb": sc.cnic_formb, 
                "address": sc.address, 
                "registration_date": sc.registration_date,
                "course": c.name
            })

        return data
    else:
        
        if name is not None:
            query = query.filter(
                Scholarship.name.ilike(f"%{name}%")
            )
        if course_id is not None:
            query = query.filter(
                Scholarship.course_id == course_id
            )
        results = query.order_by(Scholarship.id).all()

        # -- jesonfiy --
        data = []
        for sc, c in results:
            data.append({
                "id" : sc.id,
                "name": sc.name, 
                "father_name": sc.father_name, 
                "qualification": sc.qualification, 
                "whatsapp": sc.whatsapp, 
                "current_institute": sc.current_institute,
                "cnic_formb": sc.cnic_formb, 
                "address": sc.address, 
                "registration_date": sc.registration_date,
                "course": c.name
            })
        return data

    results = query.order_by(Scholarship.id).all()
    # -- jesonfiy --
    data = []
    for sc, c in results:
        data.append({
            "id" : sc.id,
            "name": sc.name, 
            "father_name": sc.father_name, 
            "qualification": sc.qualification, 
            "whatsapp": sc.whatsapp, 
            "current_institute": sc.current_institute,
            "cnic_formb": sc.cnic_formb, 
            "address": sc.address, 
            "registration_date": sc.registration_date,
            "course": c.name
        })
    return data