from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse, Response,
                                RedirectResponse, StreamingResponse)

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.helper_orm import Department

from app.models.helper_orm import (Department, Course, SalaryType,
                                    Shift, ClassCode, AdmissionType, Semester,
                                    Session, Month, Day, PaymentType, ContractType,
                                    DocType)

from app.utils.form_submission import (title_case, 
                                        validate_cnic, 
                                        validate_phone_number
                                    )

helper_add_router = APIRouter(prefix="/helper", tags=["Helper"])
templates = Jinja2Templates("frontend")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ==============================================================================#
#      L O A D    --    A D D      --     D E L E T E     C O U R S E           #
# ==============================================================================#
@helper_add_router.get("/course_form", response_class=HTMLResponse)
async def course_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "pages/helper_add/add_course.html",
        {"request": request}
    )


@helper_add_router.post("/add_course")
async def add_course(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()
    department_id = form_data.get("department_id")
    course_name = title_case(form_data.get("course_name")) if form_data.get("course_name") else ""

    new_course = Course(
        name=course_name,
        department_id=department_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return RedirectResponse(
        url="/helper/list_courses", 
        status_code=303
        )


@helper_add_router.get("/list_courses", response_class=HTMLResponse)
async def list_courses(request: Request, db: Session = Depends(get_db)):
    # -- build the query to get courses with their department names --
    results = (db.query(Course, Department)
                .join(Department, Course.department_id == Department.department_id)
                .order_by(Department.department_id)
                .all()
                )
    
    # -- jesonify the results --
    courses_json = []
    for course, department in results:
        courses_json.append({
            "course_id": course.course_id,
            "course_name": course.name,
            "department": department.department_name
        })

    return templates.TemplateResponse(
        "pages/helper_add/course_table.html",
        {
            "request": request, 
            "courses": courses_json
        }
    )

@helper_add_router.delete("/delete_course/{course_id}")
async def delete_course(
    course_id: int, 
    db: Session = Depends(get_db)
    ):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
    return RedirectResponse(
        url="/helper/list_courses", status_code=303
        )




# ==============================================================================#
#      L O A D    --    A D D      --     D E L E T E     S E S S I O N         #
# ==============================================================================#
@helper_add_router.get("/session_form", response_class=HTMLResponse)
async def session_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "pages/helper_add/add_session.html",
        {"request": request}
    )


@helper_add_router.post("/add_session")
async def add_session(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()
    session_id_ = form_data.get("session_name")[2:]

    # -- check if session with same id already exists --
    existing_session = db.query(Session).filter(Session.session_id == session_id_).order_by(Session.session_id).first()
    if existing_session:
        return HTMLResponse(content="""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h2 style="color: #cc0000;">Error: Session ID already exists</h2>
                    <p>Please go back and enter a different ID.</p>
                    <button onclick="window.history.back()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
                        ← Go Back to Form
                    </button>
                </body>
            </html>
        """, status_code=400)
    new_session = Session(
        session_id = session_id_,
        session=title_case(form_data.get("session_name")) if form_data.get("session_name") else ""
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return RedirectResponse(
        url="/helper/list_sessions", 
        status_code=303
        )


@helper_add_router.get("/list_sessions", response_class=HTMLResponse)
async def list_sessions(request: Request, db: Session = Depends(get_db)):
    sessions = db.query(Session).order_by(Session.session_id).all()
    return templates.TemplateResponse(
        "pages/helper_add/session_table.html",
        {
            "request": request, 
            "sessions": sessions
        }
    )

@helper_add_router.delete("/delete_session/{session_id}")
async def delete_session(
    session_id: int, 
    db: Session = Depends(get_db)
    ):
    session = db.query(Session).filter(Session.session_id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return RedirectResponse(
        url="/helper/list_sessions", status_code=303
        )




# ==============================================================================#
#      L O A D    --    A D D      --     D E L E T E     C L A S S _ C O D E   #
# ==============================================================================#
@helper_add_router.get("/class_code_form", response_class=HTMLResponse)
async def class_code_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "pages/helper_add/add_class_code.html",
        {"request": request}
    )    

@helper_add_router.post("/add_class_code")
async def add_class_code(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()
    class_code = form_data.get("class_code")

    new_class_code = ClassCode(
        class_code_name=class_code
    )
    db.add(new_class_code)
    db.commit()
    db.refresh(new_class_code)

    return RedirectResponse(
        url="/helper/list_class_codes",
        status_code=303
        )

@helper_add_router.get("/list_class_codes", response_class=HTMLResponse)
async def list_class_codes(request: Request, db: Session = Depends(get_db)):
    class_codes = db.query(ClassCode).order_by(ClassCode.class_code_id).all()
    return templates.TemplateResponse(
        "pages/helper_add/class_code_table.html",
        {
            "request": request, 
            "class_codes": class_codes
        }
    )

@helper_add_router.delete("/delete_class_code/{class_code_id}")
async def delete_class_code(
    class_code_id: int, 
    db: Session = Depends(get_db)
    ):
    class_code = db.query(ClassCode).filter(ClassCode.class_code_id == class_code_id).first()
    if class_code:
        db.delete(class_code)
        db.commit()

    return RedirectResponse(
        url="/helper/list_class_codes", 
        status_code=303
        )






# ==============================================================================#
#      L O A D    --    A D D      --     D E L E T E     D O C _ T Y P E       #
# ==============================================================================#
@helper_add_router.get("/doc_type_form", response_class=HTMLResponse)
async def doc_type_form(request: Request):
    return templates.TemplateResponse(
        "pages/helper_add/add_doc_type.html",
        {"request": request}
    )


@helper_add_router.post("/add_doc_type")
async def add_doc_type(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    form_data = await request.form()
    doc_type_name = form_data.get("doc_type_name")
    new_doc_type = DocType(
        doc_type_name=doc_type_name
    )
    db.add(new_doc_type)
    db.commit()
    db.refresh(new_doc_type)

    return RedirectResponse(
        url="/helper/list_doc_types",
        status_code=303
        )


@helper_add_router.get("/list_doc_types", response_class=HTMLResponse)
async def list_doc_types(request: Request, db: Session = Depends(get_db)):
    doc_types = db.query(DocType).order_by(DocType.doc_type_id).all()
    return templates.TemplateResponse(
        "pages/helper_add/doc_type_table.html",
        {
            "request": request, 
            "doc_types": doc_types
        }
    )

@helper_add_router.delete("/delete_doc_type/{doc_type_id}")
async def delete_doc_type(
    doc_type_id: int, 
    db: Session = Depends(get_db)
    ):
    doc_type = db.query(DocType).filter(DocType.doc_type_id == doc_type_id).first()
    if doc_type:
        db.delete(doc_type)
        db.commit()
    return RedirectResponse(
        url="/helper/list_doc_types", 
        status_code=303
        )