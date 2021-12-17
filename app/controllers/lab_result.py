from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    lab_results = db.query(models.LabResult).all() if is_active == '' else db.query(models.LabResult).filter(models.LabResult.is_active == is_active).all()
    return {
        "data": lab_results,
        "error": False,
        "message": "LabResults has been successfully retrieved."
    }

def get_one(id, db: Session):
    lab_result = db.query(models.LabResult).filter(models.LabResult.id == id).first()
    if not lab_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabResult with id {id} not found')
    return {
        "data": lab_result,
        "error": False,
        "message": f" LabResult with id = {id} has been successfully retrieved."
    }

def create(lab_result, db: Session):
    new_lab_result = models.LabResult(
        lab_request_id = lab_result.lab_request_id,
        specimen = lab_result.specimen,
        result = lab_result.result,
        reference = lab_result.reference,
        unit = lab_result.unit,
        detailed_result = lab_result.detailed_result,
        status = lab_result.status
    )
    db.add(new_lab_result)
    db.commit()
    db.refresh(new_lab_result)
    return {
        "data": new_lab_result,
        "error": False,
        "message": f"New LabResult with id '{new_lab_result.id}' has been successfully created."
    }

def reactivate(id, db: Session):
    lab_result = db.query(models.LabResult).filter(models.LabResult.id == id)
    if not lab_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabResult with id {id} not found')
    else:
        lab_result.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"LabResult with id '{id}' has been successfully re-activated." 
        return res

def update(id, LabResult, db: Session):
    lab_result = db.query(models.LabResult).filter(models.LabResult.id == id)
    if not lab_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabResult with id {id} not found')
    else:
        lab_result.update({
            "lab_request_id" : LabResult.lab_request_id,
            "specimen" : LabResult.specimen,
            "result" : LabResult.result,
            "reference" : LabResult.reference,
            "unit" : LabResult.unit,
            "detailed_result" : LabResult.detailed_result,
            "status" : LabResult.status,
            "is_active" : LabResult.is_active
        })
        db.commit()
        return {
            "data": LabResult,
            "error": False,
            "message": f"LabResult with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    lab_result = db.query(models.LabResult).filter(models.LabResult.id == id)
    if not lab_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabResult with id {id} not found')
    else:
        lab_result.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"LabResult with id = {id} has been successfully deleted." 
        return res