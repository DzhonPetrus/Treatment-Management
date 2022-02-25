from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    laboratory_types = db.query(models.Laboratory_type).all()  if is_active == '' else db.query(models.Laboratory_type).filter(models.Laboratory_type.is_active == is_active).all()
    return {
        "data": laboratory_types,
        "error": False,
        "message": "Laboratory_ types has been successfully retrieved."
    }

def get_one(id, db: Session):
    laboratory_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id).first()
    if not laboratory_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    return {
        "data": laboratory_type,
        "error": False,
        "message": f" Laboratory_ type with id = {id} has been successfully retrieved."
    }

def create(laboratory_type, db: Session):
    check = db.query(models.Laboratory_type).filter(models.Laboratory_type.name == laboratory_type.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Laboratory_type with name {laboratory_type.name} already exist.')
    else:
        new_laboratory_type = models.Laboratory_type(
            name = laboratory_type.name,
            description = laboratory_type.description,
            created_by = laboratory_type.created_by
        )
        db.add(new_laboratory_type)
        db.commit()
        db.refresh(new_laboratory_type)
        return {
            "data": new_laboratory_type,
            "error": False,
            "message": f"New Laboratory_ type with id '{new_laboratory_type.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    laboratory_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not laboratory_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        laboratory_type.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Laboratory_ type with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    laboratory_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not laboratory_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        laboratory_type.update({
            "name": Surgery_Type.name,
            "description": Surgery_Type.description,
            "updated_by": Surgery_Type.updated_by,
            "is_active": Surgery_Type.is_active
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Laboratory_ type with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    laboratory_type = db.query(models.Laboratory_type).filter(models.Laboratory_type.id == id)
    if not laboratory_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory_type with id {id} not found')
    else:
        laboratory_type.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Laboratory_ type with id = {id} has been successfully deleted." 
        return res
