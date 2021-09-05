from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    lab_tests = db.query(models.LabTest).all()
    return {
        "data": lab_tests,
        "error": False,
        "message": "Lab Tests has been successfully retrieved."
    }

def get_one(id, db: Session):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == id).first()
    if not lab_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabTest with id {id} not found')
    return {
        "data": lab_test,
        "error": False,
        "message": f" Lab Test with id = {id} has been successfully retrieved."
    }

def create(lab_test, db: Session):
    check = db.query(models.LabTest).filter(models.LabTest.name == lab_test.name)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'LabTest with name {lab_test.name} already exist.')
    else:
        new_lab_test = models.LabTest(
            name = lab_test.name,
            description = lab_test.description,
            price = lab_test.price
        )
        db.add(new_lab_test)
        db.commit()
        db.refresh(new_lab_test)
        return {
            "data": new_lab_test,
            "error": False,
            "message": f"New Lab Test with id '{new_lab_test.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == id)
    if not lab_test.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabTest with id {id} not found')
    else:
        lab_test.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Test with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery_Type, db: Session):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == id)
    if not lab_test.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabTest with id {id} not found')
    else:
        lab_test.update({
            "name": Surgery_Type.name,
            "description": Surgery_Type.description,
            "price": Surgery_Type.price,
            "is_active": Surgery_Type.is_active
        })
        db.commit()
        return {
            "data": Surgery_Type,
            "error": False,
            "message": f"Lab Test with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == id)
    if not lab_test.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabTest with id {id} not found')
    else:
        lab_test.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Lab Test with id = {id} has been successfully deleted." 
        return res
