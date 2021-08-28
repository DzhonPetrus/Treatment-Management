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


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TreatmentType)
def create(TreatmentType: schemas.CreateTreatmentType, db: Session = Depends(get_db)):
    return treatment_type.create(TreatmentType, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.TreatmentType)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return treatment_type.get_one(id, db)
    return templates.TemplateResponse("treatment_type.html", {"request":request, "treatment_type": treatment_type.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.TreatmentType], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return treatment_type.get_all(db)
    return templates.TemplateResponse("treatment_types.html", {"request":request, "treatment_type": jsonable_encoder(treatment_type.get_all(db))})