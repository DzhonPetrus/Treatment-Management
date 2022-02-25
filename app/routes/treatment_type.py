from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment_type
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment_type",
    # tags=['Lab_Tests']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment_types)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_type.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment_type)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_type.get_one(id, db)
    # return templates.TemplateResponse("treatment_type.html", {"request":request, "treatment_type": treatment_type.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Treatment_type: schemas.CreateTreatment_type = Depends(schemas.CreateTreatment_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment_type.created_by = current_user["id"]
    return treatment_type.create(Treatment_type, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_type.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Treatment_type: schemas.CreateTreatment_type = Depends(schemas.CreateTreatment_type.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment_type.updated_by = current_user["id"]
    return treatment_type.update(id, Treatment_type, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment_type.destroy(id, db)