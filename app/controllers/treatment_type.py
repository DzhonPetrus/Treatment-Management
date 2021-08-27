from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    treatment_type = db.query(models.TreatmentType).all()
    return treatment_type

def get_one(id, db: Session):
    treatment_type = db.query(models.TreatmentType).filter(models.TreatmentType.id == id).first()
    if not treatment_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TreatmentType with id {id} not found')
    return treatment_type

def create(treatment_type, db: Session):
    new_treatment_type = models.TreatmentType(
        name = treatment_type.name,
        room = treatment_type.room,
        description = treatment_type.description,  
        price = treatment_type.price
    )
    db.add(new_treatment_type)
    db.commit()
    db.refresh(new_treatment_type)
    return new_treatment_type