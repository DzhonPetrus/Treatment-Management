from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import surgery_type
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/surgery_type",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery_types)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_type.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery_type)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_type.get_one(id, db)
    # return templates.TemplateResponse("surgery_type.html", {"request":request, "surgery_type": surgery_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Surgery_type: schemas.CreateSurgery_type = Depends(schemas.CreateSurgery_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Surgery_type.created_by = current_user["id"]
    return surgery_type.create(Surgery_type, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Surgery_type: schemas.CreateSurgery_type = Depends(schemas.CreateSurgery_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Surgery_type.updated_by = current_user["id"]
    return surgery_type.update(id, Surgery_type, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery_type.destroy(id, db)