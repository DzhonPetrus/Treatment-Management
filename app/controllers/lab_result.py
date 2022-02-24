from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

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
    lab_result_no = (str(uuid4()).split('-')[0]).upper()
    new_lab_result = models.LabResult(
        lab_request_id = lab_result.lab_request_id,
        lab_result_no = lab_result_no,
        specimen = lab_result.specimen,
        result = lab_result.result,
        reference = lab_result.reference,
        comments = lab_result.comments,
        ordered = lab_result.ordered,
        dt_requested = lab_result.dt_requested,
        dt_received = lab_result.dt_received,
        dt_reported = lab_result.dt_reported,
        unit = lab_result.unit,
        detailed_result = lab_result.detailed_result,
        created_by = lab_result.created_by,
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
            "lab_result_no" : LabResult.lab_result_no,
            "specimen" : LabResult.specimen,
            "result" : LabResult.result,
            "reference" : LabResult.reference,
            "ordered" : LabResult.ordered,
            "comments" : LabResult.comments,
            "unit" : LabResult.unit,
            "dt_requested" : LabResult.dt_requested,
            "dt_received" : LabResult.dt_received,
            "dt_reported" : LabResult.dt_reported,
            "detailed_result" : LabResult.detailed_result,
            "status" : LabResult.status,
            "updated_by" : LabResult.updated_by,
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