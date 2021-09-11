from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment, user, patient, treatment_type
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment",
    tags=['Treatment']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatments)
def show(request: Request, db: Session = Depends(get_db)):
    return treatment.get_all(db)
    # return {
    #     "data": treatment.get_all(db),
    #     "error": False,
    #     "message": "Treatments has been successfully retrieved."
    # }

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return treatment.get_all(db)
    return templates.TemplateResponse("treatments.html", {"request":request, 'current_path': request.url.path, "treatment_types":jsonable_encoder(treatment_type.get_all(db,'ACTIVE')['data']), "patients":jsonable_encoder(patient.get_all(db,'ACTIVE')['data']), "physicians":jsonable_encoder(user.get_all(db,'ACTIVE')['data'])})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment)
def show(request: Request, id, db: Session = Depends(get_db)):
    return treatment.get_one(id, db)
    # return templates.TemplateResponse("treatment.html", {"request":request, "treatment": treatment.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Treatment: schemas.CreateTreatment = Depends(schemas.CreateTreatment.as_form), db: Session = Depends(get_db)):
    return treatment.create(Treatment, db)

@router.put('/cancel/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return treatment.cancel(id, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return treatment.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Treatment: schemas.CreateTreatment = Depends(schemas.CreateTreatment.as_form), db: Session = Depends(get_db)):
    return treatment.update(id, Treatment, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return treatment.destroy(id, db)