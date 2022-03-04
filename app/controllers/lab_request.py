from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from .. import models

def get_all(db: Session, is_active = ''):
    lab_requests = db.query(models.LabRequest).all() if is_active == '' else db.query(models.LabRequest).filter(models.LabRequest.is_active == is_active).all()
    # return lab_requests
    return {
        "data": lab_requests,
        "error": False,
        "message": "LabRequests has been successfully retrieved."
    }

def get_one(id, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id).first()
    if not lab_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    return {
        "data": lab_request,
        "error": False,
        "message": f" LabRequest with id = {id} has been successfully retrieved."
    }

def create(lab_request, db: Session):
    print(lab_request)

    request_no = 'LR-' + (str(uuid4()).split('-')[0]).upper()
    # print(request_no)

    new_lab_request = models.LabRequest(
        lab_request_no = request_no,
        lab_service_name_id = lab_request.lab_service_name_id,
        quantity = lab_request.quantity,
        inpatient_id = lab_request.inpatient_id,
        outpatient_id = lab_request.outpatient_id,
        status = lab_request.status,
        created_by = lab_request.created_by,
        is_active = lab_request.is_active
    )
    db.add(new_lab_request)
    db.commit()
    db.refresh(new_lab_request)
    return {
        "data": new_lab_request,
        "error": False,
        "message": f"New LabRequest with id '{new_lab_request.id}' has been successfully created."
    }

def cancel(id, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id)
    if not lab_request.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    else:
        lab_request.update({
            "status": "CANCELLED"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"LabRequest with id '{id}' has been successfully cancelled." 
        return res

def reactivate(id, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id)
    if not lab_request.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    else:
        lab_request.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"LabRequest with id '{id}' has been successfully re-activated." 
        return res

def update(id, LabRequest, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id)
    if not lab_request.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    else:
        lab_request.update({
            "quantity" : LabRequest.quantity,
            "inpatient_id" : LabRequest.inpatient_id,
            "outpatient_id" : LabRequest.outpatient_id,
            "lab_service_name_id" : LabRequest.lab_service_name_id,
            "status" : LabRequest.status,
            "updated_by" : LabRequest.updated_by,
            "is_active" : LabRequest.is_active
        })
        db.commit()
        return {
            "data": LabRequest,
            "error": False,
            "message": f"LabRequest with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == id)
    if not lab_request.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'LabRequest with id {id} not found')
    else:
        lab_request.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"LabRequest with id = {id} has been successfully deleted." 
        return res