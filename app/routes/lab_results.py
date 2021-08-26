from app.models import lab_results
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
    prefix="/lab_results",
    tags=['Lab Results']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LabResults)
def create(LabResults: schemas.CreateLabResults, db: Session = Depends(get_db)):
    return lab_results.create(LabResults, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LabResults)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return lab_results.get_one(id, db)
    return templates.TemplateResponse("lab_results.html", {"request":request, "lab_results": surgery_type.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.LabResults], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return lab_results.get_all(db)
    return templates.TemplateResponse("lab_results.html", {"request":request, "lab_results": jsonable_encoder(lab_results.get_all(db))})