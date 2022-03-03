from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_test_type
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_test_type",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_types)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_test_type.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLaboratory_type)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_test_type.get_one(id, db)
    # return templates.TemplateResponse("lab_test_type.html", {"request":request, "lab_test_type": lab_test_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Laboratory_type: schemas.CreateLaboratory_type = Depends(schemas.CreateLaboratory_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_type.created_by = current_user["id"]
    return lab_test_type.create(Laboratory_type, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_test_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Laboratory_type: schemas.CreateLaboratory_type = Depends(schemas.CreateLaboratory_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Laboratory_type.updated_by = current_user["id"]
    return lab_test_type.update(id, Laboratory_type, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_test_type.destroy(id, db)