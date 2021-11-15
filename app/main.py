from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from . import models, routes, roles
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

router = APIRouter()
@router.get('/')
def redirect():
    return RedirectResponse("http://127.0.0.1:8000/public")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
app.include_router(routes.authentication.router)



app.include_router(roles.public.router)



app.include_router(roles.admin.router)


app.include_router(roles.lab_technician.router)
app.include_router(roles.lab_receptionist.router)


app.include_router(roles.medical_specialist.router)


app.include_router(roles.surgery_scheduler.router)
app.include_router(roles.surgical_nurse.router)
app.include_router(roles.surgeon.router)


