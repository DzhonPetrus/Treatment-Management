from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import surgery_service
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/surgery_service",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery_services)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_service.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery_service)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_service.get_one(id, db)
    # return templates.TemplateResponse("surgery_service.html", {"request":request, "surgery_service": surgery_service.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Surgery_service: schemas.CreateSurgery_service = Depends(schemas.CreateSurgery_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Surgery_service.created_by = current_user["id"]
    return surgery_service.create(Surgery_service, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_service.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Surgery_service: schemas.CreateSurgery_service = Depends(schemas.CreateSurgery_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Surgery_service.updated_by = current_user["id"]
    return surgery_service.update(id, Surgery_service, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_service.destroy(id, db)