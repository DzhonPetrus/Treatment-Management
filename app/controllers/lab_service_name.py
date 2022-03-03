from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, status = ''):
    lab_service_name = db.query(models.LabServiceName).all()  if status == '' else db.query(models.LabServiceName).filter(models.LabServiceName.status == status).all()
    return {
        "data": lab_service_name,
        "error": False,
        "message": "Lab Services has been successfully retrieved."
    }

def get_one(id, db: Session):
    lab_service_name = db.query(models.LabServiceName).filter(models.LabServiceName.id == id).first()
    if not lab_service_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabServiceName with id {id} not found')
    return {
        "data": lab_service_name,
        "error": False,
        "message": f" Lab Service with id = {id} has been successfully retrieved."
    }

def create(lab_service_name, db: Session):
    check = db.query(models.LabServiceName).filter(models.LabServiceName.lab_service_name == lab_service_name.lab_service_name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'LabServiceName with lab_service_name {lab_service_name.lab_service_name} already exist.')
    else:
        new_lab_service_name = models.LabServiceName(
            lab_test_types_id = lab_service_name.lab_test_types_id,
            lab_service_name = lab_service_name.lab_service_name,
            description = lab_service_name.description,
            unit_price = lab_service_name.unit_price,
            created_by = lab_service_name.created_by,
        )
        db.add(new_lab_service_name)
        db.commit()
        db.refresh(new_lab_service_name)
        return {
            "data": new_lab_service_name,
            "error": False,
            "message": f"New Lab Service with id '{new_lab_service_name.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    lab_service_name = db.query(models.LabServiceName).filter(models.LabServiceName.id == id)
    if not lab_service_name.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabServiceName with id {id} not found')
    else:
        lab_service_name.update({
            "status": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    lab_service_name = db.query(models.LabServiceName).filter(models.LabServiceName.id == id)
    if not lab_service_name.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabServiceName with id {id} not found')
    else:
        lab_service_name.update({
            "lab_service_name": Surgery_Type.lab_service_name,
            "description": Surgery_Type.description,
            "unit_price": Surgery_Type.unit_price,
            "updated_by": Surgery_Type.updated_by,
            "status": Surgery_Type.status
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Lab Service with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    lab_service_name = db.query(models.LabServiceName).filter(models.LabServiceName.id == id)
    if not lab_service_name.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabServiceName with id {id} not found')
    else:
        lab_service_name.update({
            "status": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Service with id = {id} has been successfully deleted." 
        return res
