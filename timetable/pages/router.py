from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from core.models import User
from api.login import create_user


router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/registration")
async def registration_user(request: Request):     #   user = Depends(create_user)
    return templates.TemplateResponse("registration.html", {"request": request})





