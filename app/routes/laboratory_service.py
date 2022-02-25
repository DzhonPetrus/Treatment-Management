from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import laboratory_service
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/laboratory_service",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_services)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_service.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_service)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_service.get_one(id, db)
    # return templates.TemplateResponse("laboratory_service.html", {"request":request, "laboratory_service": laboratory_service.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Laboratory_service: schemas.CreateLaboratory_service = Depends(schemas.CreateLaboratory_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_service.created_by = current_user["id"]
    return laboratory_service.create(Laboratory_service, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_service.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Laboratory_service: schemas.CreateLaboratory_service = Depends(schemas.CreateLaboratory_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_service.updated_by = current_user["id"]
    return laboratory_service.update(id, Laboratory_service, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_service.destroy(id, db)