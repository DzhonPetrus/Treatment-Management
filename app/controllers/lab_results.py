from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    lab_results = db.query(models.LabResults).all()
    return lab_results

def get_one(id, db: Session):
    lab_results = db.query(models.LabResults).filter(models.LabResults.id == id).first()
    if not lab_results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabResults with id {id} not found')
    return lab_results

def create(lab_results, db: Session):
    new_lab_results = models.LabResults(
        specimen = lab_results.specimen, 
        result = lab_results.result,
        reference = lab_results.reference,
        unit = lab_results.unit,
        detailed_result = lab_results.detailed_result
    )
    db.add(new_lab_results)
    db.commit()
    db.refresh(new_lab_results)
    return new_lab_results