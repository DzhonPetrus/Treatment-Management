from .. import routes

from fastapi import APIRouter, Depends, status, Request

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)

router.include_router(routes.index.router)

router.include_router(routes.surgery.router)
router.include_router(routes.surgery_type.router)

router.include_router(routes.lab_test.router)
router.include_router(routes.laboratory_type.router)
router.include_router(routes.laboratory_service.router)

router.include_router(routes.lab_result.router)
router.include_router(routes.lab_request.router)

router.include_router(routes.treatment.router)
router.include_router(routes.treatment_type.router)

router.include_router(routes.inpatient.router)
router.include_router(routes.outpatient.router)
router.include_router(routes.user.router)
router.include_router(routes.profile.router)

router.include_router(routes.me.router)



router.include_router(routes.sysadmin.router)