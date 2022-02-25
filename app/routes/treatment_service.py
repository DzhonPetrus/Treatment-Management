from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment_service
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment_service",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment_services)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_service.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment_service)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_service.get_one(id, db)
    # return templates.TemplateResponse("treatment_service.html", {"request":request, "treatment_service": treatment_service.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Treatment_service: schemas.CreateTreatment_service = Depends(schemas.CreateTreatment_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment_service.created_by = current_user["id"]
    return treatment_service.create(Treatment_service, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_service.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Treatment_service: schemas.CreateTreatment_service = Depends(schemas.CreateTreatment_service.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment_service.updated_by = current_user["id"]
    return treatment_service.update(id, Treatment_service, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_service.destroy(id, db)