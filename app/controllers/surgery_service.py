from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    surgery_service = db.query(models.Surgery_service).all()  if is_active == '' else db.query(models.Surgery_service).filter(models.Surgery_service.is_active == is_active).all()
    return {
        "data": surgery_service,
        "error": False,
        "message": "Lab Services has been successfully retrieved."
    }

def get_one(id, db: Session):
    surgery_service = db.query(models.Surgery_service).filter(models.Surgery_service.id == id).first()
    if not surgery_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery_service with id {id} not found')
    return {
        "data": surgery_service,
        "error": False,
        "message": f" Lab Service with id = {id} has been successfully retrieved."
    }

def create(surgery_service, db: Session):
    check = db.query(models.Surgery_service).filter(models.Surgery_service.name == surgery_service.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Surgery_service with name {surgery_service.name} already exist.')
    else:
        new_surgery_service = models.Surgery_service(
            surgery_type_id = surgery_service.surgery_type_id,
            name = surgery_service.name,
            description = surgery_service.description,
            created_by = surgery_service.created_by,
        )
        db.add(new_surgery_service)
        db.commit()
        db.refresh(new_surgery_service)
        return {
            "data": new_surgery_service,
            "error": False,
            "message": f"New Lab Service with id '{new_surgery_service.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    surgery_service = db.query(models.Surgery_service).filter(models.Surgery_service.id == id)
    if not surgery_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery_service with id {id} not found')
    else:
        surgery_service.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    surgery_service = db.query(models.Surgery_service).filter(models.Surgery_service.id == id)
    if not surgery_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery_service with id {id} not found')
    else:
        surgery_service.update({
            "name": Surgery_Type.name,
            "description": Surgery_Type.description,
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
    surgery_service = db.query(models.Surgery_service).filter(models.Surgery_service.id == id)
    if not surgery_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery_service with id {id} not found')
    else:
        surgery_service.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id = {id} has been successfully deleted." 
        return res
