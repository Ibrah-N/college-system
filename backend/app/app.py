from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.admission_routes import student_router


from app.config.db_connect import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


# Mount static directory for CSS, JS, images
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include the student router
app.include_router(student_router)


@app.get("/")
def home():
    return {"message": "Welcome to the Student Management API"}
