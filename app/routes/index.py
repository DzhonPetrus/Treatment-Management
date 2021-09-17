from typing import List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from .. import database

from .. import schemas, oauth2



templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    # prefix="/lab_request",
    tags=['Home / Index']
)

get_db = database.get_db

@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def all(request: Request, db: Session = Depends(get_db)):
    current_role = request.url.path.split('/')[1]
    print(current_role)
    if current_role == 'admin':
        print(f'{current_role}/index.html')
    elif current_role == 'surgery_scheduler':
        print('zup scheduler')
    elif current_role == 'surgeon':
        print('zup doc')
    # return lab_request.get_all(db)
    return templates.TemplateResponse(f'{current_role}.index.html', {"request":request, 'current_path': request.url.path})
    # return templates.TemplateResponse(f"index.html", {"request":request, 'current_path': request.url.path})