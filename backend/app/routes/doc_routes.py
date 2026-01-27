from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates 


from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.admission_orm import Student
from app.models.doc_orm import DocsManagement

from app.models.helper_orm import DocType

from app.utils.form_submission import (title_case, 
                                        validate_phone_number
                                    )

import pandas as pd
import io

doc_router = APIRouter(prefix="/docs", tags=["Document Management"])
templates = Jinja2Templates("frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ============================================================
#          L O A D - D O C U M E N T - F O R M               #
# ============================================================
@doc_router.get("/form", response_class=HTMLResponse)
async def doc_form(request: Request):
    return templates.TemplateResponse(
        "pages/doc_management/doc_form.html", 
        {
            "request": request
        }
    )




# ============================================================
#                  L I S T -  D O C U M E N TS               #
# ============================================================
@doc_router.get("/list_docs", response_class=HTMLResponse)
async def list_docs(request: Request, db: Session = Depends(get_db)):

    # -- build query --
    query = (
        db.query(DocsManagement, DocType, Student)
        .join
        (DocType, DocsManagement.doc_type_id == DocType.doc_type_id)
        .join
        (Student, DocsManagement.student_id == Student.student_id)
    )
    docs = query.order_by(DocsManagement.id.desc()).all()

    # -- jesonify data --
    data = []
    for docs_mng, doc_type, student in docs:
        doc_dict = {
            "id": docs_mng.id,
            "student_name": student.name,
            "father_name": student.father_name,
            "doc_type_name": doc_type.doc_type_name,
            "doc_number": docs_mng.doc_number,
            "recived_by": docs_mng.recived_by,
            "reciver_phone": docs_mng.reciver_phone,
            "note": docs_mng.doc_note,
            "date": docs_mng.date
        }
        data.append(doc_dict)

    # -- render template --
    return templates.TemplateResponse(
        "pages/doc_management/doc_table.html", 
        {
            "request": request,
            "docs": data
        }
    )   




# ============================================================
#                    A D D  -  D O C U M E N T               #
# ============================================================
@doc_router.post("/submit")
async def submit_doc_form(
    request: Request,
    db: Session = Depends(get_db)
):

    # -- Extract form data --
    form_data = await request.form()
    student_id = form_data.get("student_id")
    doc_type_id = form_data.get("doc_type_id")
    doc_number = form_data.get("doc_number") if form_data.get("doc_number") else ""
    recived_by = title_case(form_data.get("recived_by")) if form_data.get("recived_by") else ""
    reciver_phone = validate_phone_number(form_data.get("reciver_phone")) if form_data.get("reciver_phone") else ""
    note = form_data.get("note") if form_data.get("note") else ""

    # -- Create new document record --
    new_doc = DocsManagement(
        student_id=student_id,
        doc_type_id=doc_type_id,
        doc_number=doc_number,
        recived_by=recived_by,
        reciver_phone=reciver_phone,
        doc_note=note
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # -- Redirect to document list --
    return RedirectResponse(
        url="/docs/list_docs", 
        status_code=303
    )




# ============================================================
#              D E L E T E -  D O C U M E N T               #
# ============================================================
@doc_router.delete("/delete_doc/{doc_id}")
async def delete_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocsManagement).filter(DocsManagement.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return RedirectResponse(
            url="/docs/list_docs",
            status_code=303
        )
    else:
        return JSONResponse(
            content={
                    "message": "Document not found."
                    }, status_code=404
                )
    


# ============================================================
#              S E A R C H  -  D O C U M E N T               #
# ============================================================
@doc_router.post("/doc_search", response_class=HTMLResponse)
async def search_docs(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    id_search = form_data.get("id_search")
    name_search = form_data.get("name_search")

    # -- build query --
    query = (
        db.query(DocsManagement, DocType, Student)
        .join
        (DocType, DocsManagement.doc_type_id == DocType.doc_type_id)
        .join
        (Student, DocsManagement.student_id == Student.student_id)
    )

    if id_search:
        query = query.filter(DocsManagement.doc_number == id_search)
    if name_search:
        query = query.filter(Student.name.ilike(f"%{name_search}%"))

    docs = query.order_by(DocsManagement.id.desc()).all()

    # -- jesonify data --
    data = []
    for docs_mng, doc_type, student in docs:
        doc_dict = {
            "id": docs_mng.id,
            "student_name": student.name,
            "father_name": student.father_name,
            "doc_type_name": doc_type.doc_type_name,
            "doc_number": docs_mng.doc_number,
            "recived_by": docs_mng.recived_by,
            "reciver_phone": docs_mng.reciver_phone,
            "note": docs_mng.doc_note,
            "date": docs_mng.date
        }
        data.append(doc_dict)

    # -- render template --
    return templates.TemplateResponse(
        "pages/doc_management/doc_table.html", 
        {
            "request": request,
            "docs": data
        }
    )


# ============================================================
#            E X P O R T -  D O C U M E N T                  #
# ============================================================
@doc_router.post("/export_docs")
async def export_docs(
    request: Request,
    db: Session = Depends(get_db)
):

    form_data = await request.form()
    id_search = form_data.get("id_search")
    name_search = form_data.get("name_search")

    # -- build query --
    query = (
        db.query(DocsManagement, DocType, Student)
        .join
        (DocType, DocsManagement.doc_type_id == DocType.doc_type_id)
        .join
        (Student, DocsManagement.student_id == Student.student_id)
    )

    if id_search:
        query = query.filter(DocsManagement.doc_number == id_search)
    if name_search:
        query = query.filter(Student.name.ilike(f"%{name_search}%"))

    docs = query.order_by(DocsManagement.id.desc()).all()

    # -- jesonify data --
    data = []
    for docs_mng, doc_type, student in docs:
        doc_dict = {
            "id": docs_mng.id,
            "student_name": student.name,
            "father_name": student.father_name,
            "doc_type_name": doc_type.doc_type_name,
            "doc_number": docs_mng.doc_number,
            "recived_by": docs_mng.recived_by,
            "reciver_phone": docs_mng.reciver_phone,
            "note": docs_mng.doc_note,
            "date": docs_mng.date
        }
        data.append(doc_dict)


    # -- write csv --
    df = pd.DataFrame(data)

    # # --- Export as Excel ---
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=doc_export.csv"}
    )

