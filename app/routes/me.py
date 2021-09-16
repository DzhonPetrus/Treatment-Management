from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database, schemas, oauth2

from ..controllers import user



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/me",
    tags=['Me']
)

get_db = database.get_db

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return user.get_all(db)
    return templates.TemplateResponse("me.html", {"request":request, 'current_path': request.url.path})