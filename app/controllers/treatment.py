from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    treatment = db.query(models.Treatment).all()
    return treatment

def get_one(id, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id).first()
    if not treatment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    return treatment

def create(treatment, db: Session):
    new_treatment = models.Treatment(
        description = treatment.description,
        status = treatment.status
        
        
    )
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return new_treatment