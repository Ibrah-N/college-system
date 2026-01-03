from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse,
                                RedirectResponse, StreamingResponse)




login_router = APIRouter(prefix="/main", tags=["Login Routes"])
templates = Jinja2Templates("frontend")

@login_router.get("/list_form", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Render the main login page with module cards and function buttons.
    """
    return templates.TemplateResponse("pages/main_login/form_main.html", {"request": request})


@login_router.post("/login", response_class=HTMLResponse)
async def authenticate_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # Dummy credentials (replace later with DB check)
    if username == "admin" and password == "password":
        return RedirectResponse(
            url="/main/list_form",
            status_code=302
        )

    # Incorrect credentials → return login page with error
    return templates.TemplateResponse(
        "pages/main_login/login.html",
        {
            "request": request,
            "error": "Incorrect username or password"
        },
        status_code=401
    )