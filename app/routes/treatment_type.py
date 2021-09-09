from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment_type
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment_type",
    tags=['Treatment Types']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatmentTypes)
def show(request: Request, db: Session = Depends(get_db)):
    return treatment_type.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse, response_model=schemas.OutTreatmentType)
def all(request: Request, db: Session = Depends(get_db)):
    # return treatment_type.get_all(db)
    return templates.TemplateResponse("treatment_types.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK)
def show(request: Request, id, db: Session = Depends(get_db)):
    return treatment_type.get_one(id, db)
    # return templates.TemplateResponse("treatment_type.html", {"request":request, "treatment_type": treatment_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(TreatmentType: schemas.CreateTreatmentType = Depends(schemas.CreateTreatmentType.as_form), db: Session = Depends(get_db)):
    return treatment_type.create(TreatmentType, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return treatment_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, TreatmentType: schemas.CreateTreatmentType = Depends(schemas.CreateTreatmentType.as_form), db: Session = Depends(get_db)):
    return treatment_type.update(id, TreatmentType, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return treatment_type.destroy(id, db)
