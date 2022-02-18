from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database, schemas, oauth2

from ..controllers import inpatient



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/inpatient",
    # tags=['InPatients']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutInPatients)
def all(request: Request, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return inpatient.get_all(db)
    return templates.TemplateResponse("inpatients.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutInPatient)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.get_one(id, db)
    # return templates.TemplateResponse("inpatient.html", {"request":request, "inpatient": inpatient.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(InPatient: schemas.CreateInPatient = Depends(schemas.CreateInPatient.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.create(InPatient, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, InPatient: schemas.CreateInPatient = Depends(schemas.CreateInPatient.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.update(id, InPatient, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return inpatient.destroy(id, db)
