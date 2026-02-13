from fastapi import APIRouter, Depends, Request
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

from app.utils.form_submission import (title_case, 
                                        validate_cnic,
                                        validate_phone_number
                                    )

import pandas as pd
import io
from datetime import datetime



# -- add paths --
scholarship_utils_router = APIRouter(prefix="/scholarship", tags=["Scholarship"])
templates = Jinja2Templates(directory="frontend")


# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ============================================================
#              L O A D - T E S T _ I N F O                   #
# ============================================================
@scholarship_utils_router.get("/testinfo_form", response_class=JSONResponse)
async def get_testinfo_form(
    request: Request, 
    db: Session = Depends(get_db)
    ):

    return templates.TemplateResponse(
        "pages/scholarship/testinfo_form.html", 
        {
            "request": request
        }
    )



# ============================================================
#              L I S T - T E S T _ I N F O.                  #
# ============================================================
@scholarship_utils_router.get("/list_testinfo", response_class=JSONResponse)
async def list_testinfo(
    request: Request, 
    db: Session = Depends(get_db)
    ):

    testinfo_records = db.query(TestInfo).order_by(TestInfo.id.desc()).all()

    results = []
    for record in testinfo_records:
        results.append(
            {
                "id": record.id,
                "center": record.center,
                "test_date_1": record.test_date_1,
                "test_date_2": record.test_date_2,
                "time_1": record.time_1,
                "time_2": record.time_2
            }
        )

    return templates.TemplateResponse(
        "pages/scholarship/testinfo_table.html",
        {
            "request": request,
            "testinfo_records": results
        }
    )



# ============================================================
#              A D D - T E S T _ I N F O.                    #
# ============================================================
@scholarship_utils_router.post("/add_testinfo", response_class=RedirectResponse)
async def add_testinfo(
    request: Request,
    db: Session = Depends(get_db)
    ):

    form_data = await request.form()

    print("Form Data:", form_data)
    center = title_case(form_data.get("name")) if form_data.get("name") else ""
    test_date_1 = form_data.get("date1")
    test_date_2 = form_data.get("date2")
    time_1 = form_data.get("time1")
    time_2 = form_data.get("time2")

    new_testinfo = TestInfo(
        center=center,
        test_date_1=test_date_1,
        test_date_2=test_date_2,
        time_1=time_1,
        time_2=time_2
    )

    db.add(new_testinfo)
    db.commit()

    return RedirectResponse(
        url="/scholarship/list_testinfo", 
        status_code=303
    )



# ============================================================
#              D E L E T E - T E S T _ I N F O.              #
# ============================================================
@scholarship_utils_router.delete("/delete_testinfo/{id}", response_class=RedirectResponse)
async def delete_testinfo(
    id: int,
    db: Session = Depends(get_db)
    ):

    testinfo_record = db.query(TestInfo).filter(TestInfo.id == id).first()

    if testinfo_record:
        db.delete(testinfo_record)
        db.commit()

    return RedirectResponse(
        url="/scholarship/list_testinfo", 
        status_code=303
    )




# ============================================================
#             L O A D  - S Y L L A B U S _ I N F O           #
# ============================================================
@scholarship_utils_router.get("/syllabus_form", response_class=JSONResponse)
async def get_syllabus_form(
    request: Request, 
    db: Session = Depends(get_db)
    ):

    return templates.TemplateResponse(
        "pages/scholarship/syllabus_form.html", 
        {
            "request": request
        }
    )


# ============================================================
#              L I S T - S Y L L A B U S _ I N F O           #
# ============================================================
@scholarship_utils_router.get("/list_syllabus", response_class=JSONResponse)
async def list_syllabus(
    request: Request, 
    db: Session = Depends(get_db)
    ):

    syllabus_records = db.query(SyllabusInfo).order_by(SyllabusInfo.syllabus_id.desc()).all()

    results = []
    for record in syllabus_records:
        results.append(
            {
                "id": record.syllabus_id,
                "subject_1": record.chemisty,
                "subject_2": record.physics,
                "subject_3": record.english,
                "subject_4": record.general
            }
        )

    return templates.TemplateResponse(
        "pages/scholarship/syllabus_table.html",
        {
            "request": request,
            "syllabus_records": results
        }
    )


# ============================================================
#              A D D - S Y L L A B U S _ I N F O           #
# ============================================================
@scholarship_utils_router.post("/add_syllabus", response_class=RedirectResponse)
async def add_syllabus(
    request: Request,
    db: Session = Depends(get_db)
    ):

    form_data = await request.form()
    chemistry_mcqs = form_data.get("chemistry_mcqs") if form_data.get("chemistry_mcqs") else ""
    physics_mcqs = form_data.get("physics_mcqs") if form_data.get("physics_mcqs") else ""
    english_mcqs = form_data.get("english_mcqs") if form_data.get("english_mcqs") else ""
    general_mcqs = form_data.get("general_mcqs") if form_data.get("general_mcqs") else ""

    new_syllabus = SyllabusInfo(
        chemisty=chemistry_mcqs,
        physics=physics_mcqs,
        english=english_mcqs,
        general=general_mcqs
    )


    db.add(new_syllabus)
    db.commit()

    return RedirectResponse(
        url="/scholarship/list_syllabus", 
        status_code=303
    )


# ============================================================
#              D E L E T E - S Y L L A B U S _ I N F O      #
# ============================================================
@scholarship_utils_router.delete("/delete_syllabus/{id}", response_class=RedirectResponse)
async def delete_syllabus(
    id: int,
    db: Session = Depends(get_db)
    ):

    syllabus_record = db.query(SyllabusInfo).filter(SyllabusInfo.syllabus_id == id).first()

    if syllabus_record:
        db.delete(syllabus_record)
        db.commit()

    return RedirectResponse(
        url="/scholarship/list_syllabus", 
        status_code=303
    )
