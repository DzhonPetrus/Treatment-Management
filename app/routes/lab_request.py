from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_request, lab_test, lab_result, patient
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_request",
    tags=['Lab Request']
)

get_db = database.get_db


@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLabRequests)
def show(request: Request, db: Session = Depends(get_db)):
    return lab_request.get_all(db)
    # return {
    #     "data": lab_request.get_all(db),
    #     "error": False,
    #     "message": "LabRequests has been successfully retrieved."
    # }

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return lab_request.get_all(db)
    return templates.TemplateResponse("lab_requests.html", {"request":request, 'current_path': request.url.path, "lab_tests":jsonable_encoder(lab_test.get_all(db,'ACTIVE')['data']), 'lab_results':jsonable_encoder(lab_result.get_all(db,'ACTIVE')['data']), 'patients':jsonable_encoder(patient.get_all(db,'ACTIVE')['data'])})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLabRequest)
def show(request: Request, id, db: Session = Depends(get_db)):
    return lab_request.get_one(id, db)
    # return templates.TemplateResponse("lab_request.html", {"request":request, "lab_request": lab_request.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(LabRequest: schemas.CreateLabRequest = Depends(schemas.CreateLabRequest.as_form), db: Session = Depends(get_db)):
    return lab_request.create(LabRequest, db)

@router.put('/cancel/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return lab_request.cancel(id, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db)):
    return lab_request.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, LabRequest: schemas.CreateLabRequest = Depends(schemas.CreateLabRequest.as_form), db: Session = Depends(get_db)):
    return lab_request.update(id, LabRequest, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    return lab_request.destroy(id, db)