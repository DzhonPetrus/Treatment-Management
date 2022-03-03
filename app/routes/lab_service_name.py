from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_service_name
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_service_name",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLabServiceNames)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_service_name.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLabServiceName)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_service_name.get_one(id, db)
    # return templates.TemplateResponse("lab_service_name.html", {"request":request, "lab_service_name": lab_service_name.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(LabServiceName: schemas.CreateLabServiceName = Depends(schemas.CreateLabServiceName.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    LabServiceName.created_by = current_user["id"]
    return lab_service_name.create(LabServiceName, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_service_name.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, LabServiceName: schemas.CreateLabServiceName = Depends(schemas.CreateLabServiceName.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    LabServiceName.updated_by = current_user["id"]
    return lab_service_name.update(id, LabServiceName, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_service_name.destroy(id, db)