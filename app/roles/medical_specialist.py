from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/medical_specialist",
    tags=['Medical Specialist']
)

router.include_router(routes.treatment.router)
router.include_router(routes.treatment_type.router)