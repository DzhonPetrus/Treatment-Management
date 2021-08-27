from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    lab_tests = db.query(models.LabTest).all()
    return lab_tests

def get_one(id, db: Session):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == id).first()
    if not lab_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Laboratory Test with id {id} not found')
    return lab_test

def create(lab_test, db: Session):
    new_lab_test = models.LabTest(
        name = lab_test.name,
        description = lab_test.description,
        price = lab_test.price
    )
    db.add(new_lab_test)
    db.commit()
    db.refresh(new_lab_test)
    return new_lab_test