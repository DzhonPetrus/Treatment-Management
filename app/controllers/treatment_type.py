from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, status = ''):
    treatment_types = db.query(models.Treatment_type).all()  if status == '' else db.query(models.Treatment_type).filter(models.Treatment_type.status == status).all()
    return {
        "data": treatment_types,
        "error": False,
        "message": "Treatment_ types has been successfully retrieved."
    }

def get_one(id, db: Session):
    treatment_type = db.query(models.Treatment_type).filter(models.Treatment_type.id == id).first()
    if not treatment_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_type with id {id} not found')
    return {
        "data": treatment_type,
        "error": False,
        "message": f" Treatment_ type with id = {id} has been successfully retrieved."
    }

def create(treatment_type, db: Session):
    check = db.query(models.Treatment_type).filter(models.Treatment_type.treatment_type_name == treatment_type.treatment_type_name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Treatment_type with treatment_type_name {treatment_type.treatment_type_name} already exist.')
    else:
        new_treatment_type = models.Treatment_type(
            treatment_type_name = treatment_type.treatment_type_name,
            description = treatment_type.description,
            created_by = treatment_type.created_by
        )
        db.add(new_treatment_type)
        db.commit()
        db.refresh(new_treatment_type)
        return {
            "data": new_treatment_type,
            "error": False,
            "message": f"New Treatment_ type with id '{new_treatment_type.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    treatment_type = db.query(models.Treatment_type).filter(models.Treatment_type.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_type with id {id} not found')
    else:
        treatment_type.update({
            "status": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment_ type with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    treatment_type = db.query(models.Treatment_type).filter(models.Treatment_type.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_type with id {id} not found')
    else:
        treatment_type.update({
            "treatment_type_name": Surgery_Type.treatment_type_name,
            "description": Surgery_Type.description,
            "updated_by": Surgery_Type.updated_by,
            "status": Surgery_Type.status
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Treatment_ type with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    treatment_type = db.query(models.Treatment_type).filter(models.Treatment_type.id == id)
    if not treatment_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment_type with id {id} not found')
    else:
        treatment_type.update({
            "status": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment_ type with id = {id} has been successfully deleted." 
        return res
