from app.utils.file_upload import file_upload
from typing import List
from fastapi import APIRouter, Depends, status, Request, UploadFile, File
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import lab_result
from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/lab_result",
    tags=['Lab Results']
)

get_db = database.get_db


@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutLabResults)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_result.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return lab_result.get_all(db)
    return templates.TemplateResponse("lab_results.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutLabResult)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_result.get_one(id, db)
    # return templates.TemplateResponse("lab_result.html", {"request":request, "lab_result": lab_result.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(LabResult: schemas.CreateLabResult = Depends(schemas.CreateLabResult.as_form), file: UploadFile = File(...), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    LabResult.detailed_result = await file_upload(file)
    return lab_result.create(LabResult, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_result.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
async def update(id, LabResult: schemas.CreateLabResult = Depends(schemas.CreateLabResult.as_form),file: UploadFile = File(...), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    LabResult.detailed_result = await file_upload(file)
    return lab_result.update(id, LabResult, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return lab_result.destroy(id, db)