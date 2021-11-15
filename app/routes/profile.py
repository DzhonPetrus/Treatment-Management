from typing import List
from fastapi import APIRouter, Depends, status, Request, UploadFile, File
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import profile
from .. import schemas, oauth2
from ..utils.file_upload import file_upload


templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/profile",
    # tags=['Profiles']
)

get_db = database.get_db


@router.get('/all', status_code=status.HTTP_200_OK, response_model=schemas.OutProfiles)
def show(request: Request, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.get_all(db)

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return profile.get_all(db)
    return templates.TemplateResponse("profiles.html", {"request":request, 'current_path': request.url.path})

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutProfile)
def show(request: Request, id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.get_one(id, db)
    # return templates.TemplateResponse("profile.html", {"request":request, "profile": profile.get_one(id, db)})

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(Profile: schemas.CreateProfile = Depends(schemas.CreateProfile.as_form), file: UploadFile = File(...), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Profile.photo_url = await file_upload(file)
    return profile.create(Profile, db)

@router.put('/reactivate/{id}', status_code=status.HTTP_200_OK)
def update(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.reactivate(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
async def update(id, Profile: schemas.CreateProfile = Depends(schemas.CreateProfile.as_form), file: UploadFile = File(...), db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    Profile.photo_url = await file_upload(file)
    return profile.update(id, Profile, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profile.destroy(id, db)