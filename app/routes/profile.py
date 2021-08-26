from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from ..controllers import profile
from .. import schemas



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/profile",
    tags=['Profiles']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Profile)
def create(Profile: schemas.CreateProfile, db: Session = Depends(get_db)):
    return profile.create(Profile, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Profile)
def show(request: Request, id, db: Session = Depends(get_db)):
    # return profile.get_one(id, db)
    return templates.TemplateResponse("profile.html", {"request":request, "profile": profile.get_one(id, db)})

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Profile], response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return profile.get_all(db)
    return templates.TemplateResponse("Profiles.html", {"request":request, "profiles": jsonable_encoder(profile.get_all(db))})