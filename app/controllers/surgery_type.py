from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    surgery_types = db.query(models.SurgeryType).all()
    return {
        "data": surgery_types,
        "error": False,
        "message": "Successfully retreived all Surgery Types"
    }

def get_one(id, db: Session):
    surgery_type = db.query(models.SurgeryType).filter(models.SurgeryType.id == id).first()
    if not surgery_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'SurgeryType with id {id} not found')
    return {
        "data": surgery_type,
        "error": False,
        "message": f"Successfully retreived  Surgery Type with id = {id}"
    }

def create(surgery_type, db: Session):
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
        "message": "Successfully created new surgery type"
    }