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
    check = db.query(models.Treatment_service).filter(models.Treatment_service.name == treatment_service.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Treatment_service with name {treatment_service.name} already exist.')
    else:
        new_treatment_service = models.Treatment_service(
            treatment_type_id = treatment_service.treatment_type_id,
            name = treatment_service.name,
            description = treatment_service.description,
            fee = treatment_service.fee,
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
            "name": Surgery_Type.name,
            "description": Surgery_Type.description,
            "fee": Surgery_Type.fee,
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
