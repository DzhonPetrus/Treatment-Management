from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/surgeon",
    tags=['Surgeon']
)

router.include_router(routes.surgery.router)
router.include_router(routes.surgery_type.router)