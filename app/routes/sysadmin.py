from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from app import routes

from .. import database

from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/sysadmin",
    tags=['SysAdmin']
)

router.include_router(routes.user.router)
router.include_router(routes.profile.router)

get_db = database.get_db

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('sysadmin.index.html', {"request":request, 'current_path': request.url.path})