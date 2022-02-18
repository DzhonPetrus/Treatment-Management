from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import surgery, surgery_type, inpatient, outpatient, user
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/surgery",
    # tags=['Surgeries']
)

get_db = database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgeries)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.get_all(db)
    # return {
    #     "data": surgery.get_all(db),
    #     "error": False,
    #     "message": "Surgeries has been successfully retrieved."
    # }

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return surgery.get_all(db)
    return templates.TemplateResponse("surgeries.html", {"request":request, 'current_path': request.url.path, "surgery_types":jsonable_encoder(surgery_type.get_all(db)['data']), "inpatients":jsonable_encoder(inpatient.get_all(db)['data']), "outpatients":jsonable_encoder(outpatient.get_all(db)['data']), "nurses":jsonable_encoder(user.get_all(db,'','Surgical_Nurse')['data']), "surgeons":jsonable_encoder(user.get_all(db, '', 'Surgeon')['data'])})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutSurgery)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.get_one(id, db)
    # return templates.TemplateResponse("surgery.html", {"request":request, "surgery": surgery.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(Surgery: schemas.CreateSurgery = Depends(schemas.CreateSurgery.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    # print(Surgery)
    return surgery.create(Surgery, db)

@router.put('/cancel/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.cancel(id, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id, Surgery: schemas.CreateSurgery = Depends(schemas.CreateSurgery.as_form), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.update(id, Surgery, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return surgery.destroy(id, db)