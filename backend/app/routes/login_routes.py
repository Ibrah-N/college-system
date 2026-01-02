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

