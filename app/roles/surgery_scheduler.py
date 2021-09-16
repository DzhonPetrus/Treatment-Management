from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/surgery_scheduler",
    tags=['Surgery Scheduler']
)

router.include_router(routes.index.router)

router.include_router(routes.surgery.router)
router.include_router(routes.surgery_type.router)

router.include_router(routes.me.router)