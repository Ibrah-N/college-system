from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# -- routers --
from app.routes.admission_routes import admission_router
from app.routes.add_teacher_routes import add_teacher_router
from app.routes.student_enrollment_routes import enrollment_router
from app.routes.helper_routes import helper_router


from app.config.db_connect import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


# Mount static directory for CSS, JS, images
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include the student router
app.include_router(admission_router)
app.include_router(enrollment_router)
app.include_router(helper_router)
app.include_router(add_teacher_router)


@app.get("/")
def home():
    return {"message": "Welcome to the Student Management API"}
