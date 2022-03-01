from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    treatment_service = db.query(models.Treatment_service).all()  if is_active == '' else db.query(models.Treatment_service).filter(models.Treatment_service.is_active == is_active).all()
    return {
        "data": treatment_service,
        "error": False,
        "message": "Lab Services has been successfully retrieved."
    }

def get_one(id, db: Session):
    treatment_service = db.query(models.Treatment_service).filter(models.Treatment_service.id == id).first()
    if not treatment_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_service with id {id} not found')
    return {
        "data": treatment_service,
        "error": False,
        "message": f" Lab Service with id = {id} has been successfully retrieved."
    }

def create(treatment_service, db: Session):
    check = db.query(models.Treatment_service).filter(models.Treatment_service.treatment_service_name == treatment_service.treatment_service_name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Treatment_service with treatment_service_name {treatment_service.treatment_service_name} already exist.')
    else:
        new_treatment_service = models.Treatment_service(
            treatment_types_id = treatment_service.treatment_types_id,
            treatment_service_name = treatment_service.treatment_service_name,
            description = treatment_service.description,
            unit_price = treatment_service.unit_price,
            created_by = treatment_service.created_by,
        )
        db.add(new_treatment_service)
        db.commit()
        db.refresh(new_treatment_service)
        return {
            "data": new_treatment_service,
            "error": False,
            "message": f"New Lab Service with id '{new_treatment_service.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    treatment_service = db.query(models.Treatment_service).filter(models.Treatment_service.id == id)
    if not treatment_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_service with id {id} not found')
    else:
        treatment_service.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    treatment_service = db.query(models.Treatment_service).filter(models.Treatment_service.id == id)
    if not treatment_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_service with id {id} not found')
    else:
        treatment_service.update({
            "treatment_service_name": Surgery_Type.treatment_service_name,
            "description": Surgery_Type.description,
            "unit_price": Surgery_Type.unit_price,
            "updated_by": Surgery_Type.updated_by,
            "is_active": Surgery_Type.is_active
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Lab Service with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    treatment_service = db.query(models.Treatment_service).filter(models.Treatment_service.id == id)
    if not treatment_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_service with id {id} not found')
    else:
        treatment_service.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id = {id} has been successfully deleted." 
        return res
