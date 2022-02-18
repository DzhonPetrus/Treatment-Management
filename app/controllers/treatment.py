from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from .. import models

def get_all(db: Session, is_active = ''):
    treatments = db.query(models.Treatment).all() if is_active == '' else db.query(models.Treatment).filter(models.Treatment.is_active == is_active).all()
    # return treatments
    return {
        "data": treatments,
        "error": False,
        "message": "Treatments has been successfully retrieved."
    }

def get_one(id, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id).first()
    if not treatment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    return {
        "data": treatment,
        "error": False,
        "message": f" Treatment with id = {id} has been successfully retrieved."
    }

def create(treatment, db: Session):

    _treatment_no = 'TN-' + (str(uuid4()).split('-')[0]).upper()

    new_treatment = models.Treatment(
        treatment_no = _treatment_no,
        inpatient_id = treatment.inpatient_id,
        outpatient_id = treatment.outpatient_id,
        treatment_type_id = treatment.treatment_type_id,
        user_id = treatment.user_id,
        description = treatment.description,
        professional_fee = treatment.professional_fee,
        session_no = treatment.session_no,
        session_datetime = treatment.session_datetime,
        drug = treatment.drug,
        dose = treatment.dose,
        next_schedule = treatment.next_schedule,
        comments = treatment.comments
    )
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return {
        "data": new_treatment,
        "error": False,
        "message": f"New Treatment with id '{new_treatment.id}' has been successfully created."
    }

def cancel(id, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id)
    if not treatment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    else:
        treatment.update({
            "status": "CANCELLED"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment with id '{id}' has been successfully cancelled." 
        return res

def reactivate(id, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id)
    if not treatment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    else:
        treatment.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment with id '{id}' has been successfully re-activated." 
        return res

def update(id, Treatment, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id)
    if not treatment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    else:
        treatment.update({
            "treatment_no" : Treatment.treatment_no,
            "inpatient_id" : Treatment.inpatient_id,
            "outpatient_id" : Treatment.outpatient_id,
            "treatment_type_id" : Treatment.treatment_type_id,
            "user_id" : Treatment.user_id,
            "description" : Treatment.description,
            "session_no" : Treatment.session_no,
            "professional_fee" : Treatment.professional_fee,
            "session_datetime" : Treatment.session_datetime,
            "drug" : Treatment.drug,
            "dose" : Treatment.dose,
            "next_schedule" : Treatment.next_schedule,
            "comments" : Treatment.comments,
            "status" : Treatment.status,
            "is_active" : Treatment.is_active
        })
        db.commit()
        return {
            "data": Treatment,
            "error": False,
            "message": f"Treatment with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    treatment = db.query(models.Treatment).filter(models.Treatment.id == id)
    if not treatment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Treatment with id {id} not found')
    else:
        treatment.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Treatment with id = {id} has been successfully deleted." 
        return res