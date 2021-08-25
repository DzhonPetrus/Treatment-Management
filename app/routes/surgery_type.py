from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import surgery_type
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/surgery_type",
    tags=['Surgery Types']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SurgeryType)
def create(SurgeryType: schemas.CreateSurgeryType, db: Session = Depends(get_db)):
    return surgery_type.create(SurgeryType, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.SurgeryType)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return surgery_type.get_one(id, db)
    return templates.TemplateResponse("surgery_type.html", {"request":request, "surgery_type": surgery_type.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.SurgeryType], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return surgery_type.get_all(db)
    return templates.TemplateResponse("surgery_types.html", {"request":request, "surgery_types": jsonable_encoder(surgery_type.get_all(db))})