import httpx
from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import treatment, user, inpatient, outpatient, treatment_type
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/treatment",
    # tags=['Treatment']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatments)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment.get_all(db)
    # return {
    #     "data": treatment.get_all(db),
    #     "error": False,
    #     "message": "Treatments has been successfully retrieved."
    # }

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return treatment.get_all(db)
    role_path = request.url.path.split('/')[1]
    physicians = httpx.get(f'http://127.0.0.1:8001/{role_path}/user/all').json()['data']

    return templates.TemplateResponse("treatments.html", {"request":request, 'current_path': request.url.path, "inpatients":jsonable_encoder(inpatient.get_all(db,'ACTIVE')['data']), "outpatients":jsonable_encoder(outpatient.get_all(db,'ACTIVE')['data']), "physicians":jsonable_encoder(physicians)})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutTreatment)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment.get_one(id, db)
    # return templates.TemplateResponse("treatment.html", {"request":request, "treatment": treatment.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Treatment: schemas.CreateTreatment = Depends(schemas.CreateTreatment.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment.created_by = current_user["id"]
    return treatment.create(Treatment, db)

@router.put('/cancel/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment.cancel(id, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Treatment: schemas.CreateTreatment = Depends(schemas.CreateTreatment.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Treatment.updated_by = current_user["id"]
    return treatment.update(id, Treatment, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return treatment.destroy(id, db)