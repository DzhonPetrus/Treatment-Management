from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    surgery_types = db.query(models.SurgeryType).all() if is_active == '' else db.query(models.SurgeryType).filter(models.SurgeryType.is_active == is_active).all()
    return {
        "data": surgery_types,
        "error": False,
        "message": "Surgery Types has been successfully retrieved."
    }

def get_one(id, db: Session):
    surgery_type = db.query(models.SurgeryType).filter(models.SurgeryType.id == id).first()
    if not surgery_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'SurgeryType with id {id} not found')
    return {
        "data": surgery_type,
        "error": False,
        "message": f" Surgery Type with id = {id} has been successfully retrieved."
    }

def create(surgery_type, db: Session):
    check = db.query(models.SurgeryType).filter(models.SurgeryType.name == surgery_type.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'SurgeryType with name {surgery_type.name} already exist.')
    else:
        new_surgery_type = models.SurgeryType(
            name = surgery_type.name,
            description = surgery_type.description,
            price = surgery_type.price
        )
        db.add(new_surgery_type)
        db.commit()
        db.refresh(new_surgery_type)
        return {
            "data": new_surgery_type,
            "error": False,
            "message": f"New Surgery Type with id '{new_surgery_type.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    surgery_type = db.query(models.SurgeryType).filter(models.SurgeryType.id == id)
    if not surgery_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'SurgeryType with id {id} not found')
    else:
        surgery_type.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Surgery Type with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    surgery_type = db.query(models.SurgeryType).filter(models.SurgeryType.id == id)
    if not surgery_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'SurgeryType with id {id} not found')
    else:
        surgery_type.update({
            "name": Surgery_Type.name,
            "description": Surgery_Type.description,
            "price": Surgery_Type.price,
            "is_active": Surgery_Type.is_active
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Surgery Type with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    surgery_type = db.query(models.SurgeryType).filter(models.SurgeryType.id == id)
    if not surgery_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'SurgeryType with id {id} not found')
    else:
        surgery_type.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Surgery Type with id = {id} has been successfully deleted." 
        return res