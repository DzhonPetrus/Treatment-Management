from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/medical_specialist",
    tags=['Medical Specialist']
)

router.include_router(routes.index.router)
router.include_router(routes.user.router)

router.include_router(routes.treatment.router)
router.include_router(routes.treatment_type.router)
router.include_router(routes.treatment_service.router)

router.include_router(routes.me.router)