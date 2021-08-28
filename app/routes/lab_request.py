from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_request
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_request",
    tags=['Lab Request']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LabRequest)
def create(LabRequest: schemas.CreateLabRequest, db: Session = Depends(get_db)):
    return lab_request.create(LabRequest, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LabRequest)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return lab_request.get_one(id, db)
    return templates.TemplateResponse("lab_request.html", {"request":request, "lab_request": lab_request.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.LabRequest], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return lab_request.get_all(db)
    return templates.TemplateResponse("lab_request.html", {"request":request, "lab_request": jsonable_encoder(lab_request.get_all(db)), 'current_path': request.url.path})