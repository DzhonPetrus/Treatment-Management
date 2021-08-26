from app.models import lab_results
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    lab_request = db.query(models.LabRequest).all()
    return lab_request

def get_one(id, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id).first()
    if not lab_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    return lab_request

def create(lab_request, db: Session):
    new_lab_request = models.LabRequest(
        
    )
    db.add(new_lab_request)
    db.commit()
    db.refresh(new_lab_request)
    return new_lab_request