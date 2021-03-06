from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/lab_receptionist",
    tags=['Lab Receptionist']
)

router.include_router(routes.index.router)

router.include_router(routes.lab_test.router)
router.include_router(routes.lab_test_type.router)
router.include_router(routes.lab_service_name.router)

router.include_router(routes.lab_result.router)
router.include_router(routes.lab_request.router)

router.include_router(routes.me.router)