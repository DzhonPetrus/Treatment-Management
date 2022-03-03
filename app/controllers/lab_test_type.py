from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, status = ''):
    lab_test_types = db.query(models.Laboratory_type).all()  if status == '' else db.query(models.Laboratory_type).filter(models.Laboratory_type.status == status).all()
    return {
        "data": lab_test_types,
        "error": False,
        "message": "Laboratory_ types has been successfully retrieved."
    }

def get_one(id, db: Session):
    lab_test_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id).first()
    if not lab_test_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    return {
        "data": lab_test_type,
        "error": False,
        "message": f" Laboratory_ type with id = {id} has been successfully retrieved."
    }

def create(lab_test_type, db: Session):
    check = db.query(models.Laboratory_type).filter(models.Laboratory_type.lab_test_type_name == lab_test_type.lab_test_type_name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Laboratory_type with name {lab_test_type.lab_test_type_name} already exist.')
    else:
        new_lab_test_type = models.Laboratory_type(
            lab_test_type_name = lab_test_type.lab_test_type_name,
            description = lab_test_type.description,
            created_by = lab_test_type.created_by
        )
        db.add(new_lab_test_type)
        db.commit()
        db.refresh(new_lab_test_type)
        return {
            "data": new_lab_test_type,
            "error": False,
            "message": f"New Laboratory_ type with id '{new_lab_test_type.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    lab_test_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not lab_test_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        lab_test_type.update({
            "status": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Laboratory_ type with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    lab_test_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not lab_test_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        lab_test_type.update({
            "lab_test_type_name": Surgery_Type.lab_test_type_name,
            "description": Surgery_Type.description,
            "updated_by": Surgery_Type.updated_by,
            "status": Surgery_Type.status
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Laboratory_ type with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    lab_test_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not lab_test_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        lab_test_type.update({
            "status": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Laboratory_ type with id = {id} has been successfully deleted." 
        return res
