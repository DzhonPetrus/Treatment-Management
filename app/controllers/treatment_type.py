from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    treatment_types = db.query(models.TreatmentType).all()
    return {
        "data": treatment_types,
        "error": False,
        "message": "Treatment Types has been successfully retrieved."
    }

def get_one(id, db: Session):
    treatment_type = db.query(models.TreatmentType).filter(models.TreatmentType.id == id).first()
    if not treatment_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TreatmentType with id {id} not found')
    return {
        "data": treatment_type,
        "error": False,
        "message": f" Treatment Type with id = {id} has been successfully retrieved."
    }

def create(treatment_type, db: Session):
    check = db.query(models.TreatmentType).filter(models.TreatmentType.name == treatment_type.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'TreatmentType with name {treatment_type.name} already exist.')
    else:
        new_treatment_type = models.TreatmentType(
            name = treatment_type.name,
            room = treatment_type.room,
            description = treatment_type.description,
            price = treatment_type.price
        )
        db.add(new_treatment_type)
        db.commit()
        db.refresh(new_treatment_type)
        return {
            "data": new_treatment_type,
            "error": False,
            "message": f"New Treatment Type with id '{new_treatment_type.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    treatment_type = db.query(models.TreatmentType).filter(models.TreatmentType.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TreatmentType with id {id} not found')
    else:
        treatment_type.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment Type with id '{id}' has been successfully re-activated." 
        return res

def update(id, Treatment_Type, db: Session):
    treatment_type = db.query(models.TreatmentType).filter(models.TreatmentType.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TreatmentType with id {id} not found')
    else:
        treatment_type.update({
            "name": Treatment_Type.name,
            "room": Treatment_Type.room,
            "description": Treatment_Type.description,
            "price": Treatment_Type.price,
            "is_active": Treatment_Type.is_active
        })
        db.commit()
        return {
            "data": Treatment_Type,
            "error": False,
            "message": f"Treatment Type with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    treatment_type = db.query(models.TreatmentType).filter(models.TreatmentType.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TreatmentType with id {id} not found')
    else:
        treatment_type.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment Type with id = {id} has been successfully deleted." 
        return res