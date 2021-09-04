from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
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

@router.get('/all', status_code=status.HTTP_200_OK)
def show(request: Request, db: Session = Depends(get_db)):
    return surgery_type.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return surgery_type.get_all(db)
    return templates.TemplateResponse("surgery_types.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK)
def show(request: Request, id, db: Session = Depends(get_db)):
    return surgery_type.get_one(id, db)
    # return templates.TemplateResponse("surgery_type.html", {"request":request, "surgery_type": surgery_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(SurgeryType: schemas.CreateSurgeryType = Depends(schemas.CreateSurgeryType.as_form), db: Session = Depends(get_db)):
    return surgery_type.create(SurgeryType, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return surgery_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, SurgeryType: schemas.CreateSurgeryType = Depends(schemas.CreateSurgeryType.as_form), db: Session = Depends(get_db)):
    return surgery_type.update(id, SurgeryType, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return surgery_type.destroy(id, db)
