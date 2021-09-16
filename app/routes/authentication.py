from datetime import timedelta

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.jwt_token import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from .. import database, models, jwt_token
from ..utils import hashing

templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={
            "id": user.id,
            "email": user.email,
            "exp": access_token_expires
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.user_type,
        "id": user.id
    }



@router.get('/login', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    # return user.get_all(db)
    return templates.TemplateResponse("login.html", {"request":request})