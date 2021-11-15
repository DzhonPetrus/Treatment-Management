from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from app import database, schemas, oauth2

from app.controllers import user



templates = Jinja2Templates(directory="app/pages/public")

router = APIRouter(
    tags=['Landing Page']
)

get_db = database.get_db

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return user.get_all(db)
    return templates.TemplateResponse("landing.html", {"request":request, 'current_path': request.url.path})