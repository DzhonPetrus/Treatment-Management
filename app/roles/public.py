from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/public",
    tags=['Public']
)

router.include_router(routes.public.landing.router)
router.include_router(routes.public.find_doctor.router)