from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/lab_technician",
    tags=['Lab Technician']
)

router.include_router(routes.lab_test.router)
router.include_router(routes.lab_result.router)
router.include_router(routes.lab_request.router)