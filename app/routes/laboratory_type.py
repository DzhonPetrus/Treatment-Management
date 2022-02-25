from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import laboratory_type
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/laboratory_type",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_types)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_type.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_type)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_type.get_one(id, db)
    # return templates.TemplateResponse("laboratory_type.html", {"request":request, "laboratory_type": laboratory_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Laboratory_type: schemas.CreateLaboratory_type = Depends(schemas.CreateLaboratory_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_type.created_by = current_user["id"]
    return laboratory_type.create(Laboratory_type, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Laboratory_type: schemas.CreateLaboratory_type = Depends(schemas.CreateLaboratory_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_type.updated_by = current_user["id"]
    return laboratory_type.update(id, Laboratory_type, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return laboratory_type.destroy(id, db)