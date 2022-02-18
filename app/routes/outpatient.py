from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database, schemas, oauth2

from ..controllers import outpatient



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/outpatient",
    # tags=['OutPatients']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutOutPatients)
def all(request: Request, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return outpatient.get_all(db)
    return templates.TemplateResponse("outpatients.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutOutPatient)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.get_one(id, db)
    # return templates.TemplateResponse("outpatient.html", {"request":request, "outpatient": outpatient.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(OutPatient: schemas.CreateOutPatient = Depends(schemas.CreateOutPatient.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.create(OutPatient, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, OutPatient: schemas.CreateOutPatient = Depends(schemas.CreateOutPatient.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.update(id, OutPatient, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return outpatient.destroy(id, db)
