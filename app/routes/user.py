from typing import List
from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import user
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutUsers)
def show(request: Request, db: Session = Depends(get_db)):
    return user.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return user.get_all(db)
    return templates.TemplateResponse("users.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutUser)
def show(request: Request, id, db: Session = Depends(get_db)):
    return user.get_one(id, db)
    # return templates.TemplateResponse("user.html", {"request":request, "surgery_type": surgery_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(User: schemas.CreateUser = Depends(schemas.CreateUser.as_form), db: Session = Depends(get_db)):
    return user.create(User, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return user.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, User: schemas.CreateUser = Depends(schemas.CreateUser.as_form), db: Session = Depends(get_db)):
    return user.update(id, User, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return user.destroy(id, db)
