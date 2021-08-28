from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment",
    tags=['Treatment']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Treatment)
def create(Treatment: schemas.CreateTreatment, db: Session = Depends(get_db)):
    return treatment.create(Treatment, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Treatment)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return treatment.get_one(id, db)
    return templates.TemplateResponse("treatment.html", {"request":request, "treatment": treatment.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Treatment], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return treatment.get_all(db)
    return templates.TemplateResponse("treatment.html", {"request":request, "treatments": jsonable_encoder(treatment.get_all(db)), 'current_path': request.url.path})