from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/surgeon",
    tags=['Surgeon']
)

router.include_router(routes.index.router)

router.include_router(routes.surgery.router)
router.include_router(routes.surgery_type.router)
router.include_router(routes.surgery_service.router)

router.include_router(routes.me.router)