from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from app.config.db_connect import SessionLocal
from app.models.helper_orm import Department

from app.models.helper_orm import (Department, Course, SalaryType,
                                    Shift, ClassCode, AdmissionType, Semester)


helper_router = APIRouter(prefix="/helper", tags=["Helper"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@helper_router.get("/get_department")
def get_department(request: Request, db: Session = Depends(get_db)):
    departments_data = db.query(Department).all()

    # -- jsonify the data --
    departments_json = [{"id": d.department_id, "department": d.department_name}
                        for d in departments_data]

    return JSONResponse(content={"departments": departments_json})



@helper_router.get("/get_courses")
def get_courses(department_id: int, db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.department_id == department_id).all()
    return JSONResponse(
        content={
            "courses": [
                {"id": c.course_id, "name": c.name} for c in courses
            ]
        }
    )


@helper_router.get("/get_shift")
def get_shift(db: Session = Depends(get_db)):
    shift = db.query(Shift).all()
    
    return JSONResponse(
        content={
            "shift": [
                {"id": c.shift_id, "name": c.shift_name} for c in shift
            ]
        }
    )


@helper_router.get("/get_class_code")
def get_class_code(db: Session = Depends(get_db)):
    class_codes = db.query(ClassCode).all()
    return JSONResponse(
        content={
            "class_codes": [
                {"id": c.class_code_id, "name": c.class_code_name} for c in class_codes
            ]
        }
    )


@helper_router.get("/get_admission_type")
def get_admission_type(db: Session = Depends(get_db)):
    admission_type = db.query(AdmissionType).all()
    return JSONResponse(
        content={
            "admission_type": [
                {"id": c.admission_type_id, "name": c.admission_type} for c in admission_type
            ]
        }
    )

@helper_router.get("/get_semester")
def get_semester(db: Session = Depends(get_db)):
    semesters = db.query(Semester).all()
    return JSONResponse(
        content={
            "semesters": [
                {"id": c.semester_id, "name": c.semester} for c in semesters
            ]
        }
    )

@helper_router.get("/get_salary_type")
def get_salary_type(db: Session = Depends(get_db)):
    salary_types = db.query(SalaryType).all()

    return JSONResponse(
        content={
            "salary_type" : [
                {"id": s_t.salary_type_id, "name": s_t.salary_type_name} for s_t in salary_types
            ]
        }
    )

    