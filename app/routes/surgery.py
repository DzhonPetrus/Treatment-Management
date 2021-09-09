from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import surgery, surgery_type, patient
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/surgery",
    tags=['Surgeries']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgeries)
def show(request: Request, db: Session = Depends(get_db)):
    return surgery.get_all(db)
    # return {
    #     "data": surgery.get_all(db),
    #     "error": False,
    #     "message": "Surgeries has been successfully retrieved."
    # }

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return surgery.get_all(db)
    return templates.TemplateResponse("surgeries.html", {"request":request, 'current_path': request.url.path, "surgery_types":jsonable_encoder(surgery_type.get_all(db)['data']), "patients":jsonable_encoder(patient.get_all(db)['data'])})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery)
def show(request: Request, id, db: Session = Depends(get_db)):
    return surgery.get_one(id, db)
    # return templates.TemplateResponse("surgery.html", {"request":request, "surgery": surgery.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Surgery: schemas.CreateSurgery = Depends(schemas.CreateSurgery.as_form), db: Session = Depends(get_db)):
    return surgery.create(Surgery, db)

@router.put('/cancel/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return surgery.cancel(id, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return surgery.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Surgery: schemas.CreateSurgery = Depends(schemas.CreateSurgery.as_form), db: Session = Depends(get_db)):
    return surgery.update(id, Surgery, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return surgery.destroy(id, db)