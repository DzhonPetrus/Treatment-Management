from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    surgeries = db.query(models.Surgery).all()
    return surgeries

def get_one(id, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id).first()
    if not surgery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    return surgery

def create(surgery, db: Session):
    new_surgery = models.Surgery(
        # patient_id = surgery.patient_id,
        # room_id = surgery.room_id,
        # surgery_type_id = surgery.surgery_type_id,
        start_time = surgery.start_time,
        end_time = surgery.end_time
    )
    db.add(new_surgery)
    db.commit()
    db.refresh(new_surgery)
    return new_surgery