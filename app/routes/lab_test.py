from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_test
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_test",
    tags=['Lab_Tests']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LabTest)
def create(LabTest: schemas.CreateLabTest, db: Session = Depends(get_db)):
    return lab_test.create(LabTest, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LabTest)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return lab_test.get_one(id, db)
    return templates.TemplateResponse("lab_test.html", {"request":request, "lab_test": lab_test.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.LabTest], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return lab_test.get_all(db)
    return templates.TemplateResponse("lab_tests.html", {"request":request, "lab_tests": jsonable_encoder(lab_test.get_all(db)), 'current_path': request.url.path})