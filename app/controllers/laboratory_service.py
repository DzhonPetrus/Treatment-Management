from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    laboratory_service = db.query(models.Laboratory_service).all()  if is_active == '' else db.query(models.Laboratory_service).filter(models.Laboratory_service.is_active == is_active).all()
    return {
        "data": laboratory_service,
        "error": False,
        "message": "Lab Services has been successfully retrieved."
    }

def get_one(id, db: Session):
    laboratory_service = db.query(models.Laboratory_service).filter(models.Laboratory_service.id == id).first()
    if not laboratory_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_service with id {id} not found')
    return {
        "data": laboratory_service,
        "error": False,
        "message": f" Lab Service with id = {id} has been successfully retrieved."
    }

def create(laboratory_service, db: Session):
    check = db.query(models.Laboratory_service).filter(models.Laboratory_service.name == laboratory_service.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Laboratory_service with name {laboratory_service.name} already exist.')
    else:
        new_laboratory_service = models.Laboratory_service(
            laboratory_type_id = laboratory_service.laboratory_type_id,
            name = laboratory_service.name,
            description = laboratory_service.description,
            fee = laboratory_service.fee,
            created_by = laboratory_service.created_by,
        )
        db.add(new_laboratory_service)
        db.commit()
        db.refresh(new_laboratory_service)
        return {
            "data": new_laboratory_service,
            "error": False,
            "message": f"New Lab Service with id '{new_laboratory_service.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    laboratory_service = db.query(models.Laboratory_service).filter(models.Laboratory_service.id == id)
    if not laboratory_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_service with id {id} not found')
    else:
        laboratory_service.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    laboratory_service = db.query(models.Laboratory_service).filter(models.Laboratory_service.id == id)
    if not laboratory_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_service with id {id} not found')
    else:
        laboratory_service.update({
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
    laboratory_service = db.query(models.Laboratory_service).filter(models.Laboratory_service.id == id)
    if not laboratory_service.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_service with id {id} not found')
    else:
        laboratory_service.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id = {id} has been successfully deleted." 
        return res
