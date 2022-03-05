from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    inpatients = db.query(models.InPatient).all() if is_active == '' else db.query(models.InPatient).filter(models.InPatient.is_active == is_active).all()
    return {
        "data": inpatients,
        "error": False,
        "message": "InPatients has been successfully retrieved."
    }

def get_one(id, db: Session):
    inpatient = db.query(models.InPatient).filter(models.InPatient.id == id).first()
    if not inpatient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'InPatient with id {id} not found')
    return {
        "data": inpatient,
        "error": False,
        "message": f" InPatient with id = {id} has been successfully retrieved."
    }

def create(inpatient, db: Session):
    check = db.query(models.InPatient).filter(models.InPatient.email == inpatient.email)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'InPatient with email {inpatient.email} already exist.')
    else:
        new_inpatient = models.InPatient(
            first_name = inpatient.first_name,
            middle_name = inpatient.middle_name,
            last_name = inpatient.last_name,
            suffix_name = inpatient.suffix_name,
            birth_date = inpatient.birth_date,
            gender = inpatient.gender,
            contact_no = inpatient.contact_no,
            email = inpatient.email,
            blood_type = inpatient.blood_type,
            diagnosis = inpatient.diagnosis,
            tests = inpatient.tests,
            treatments = inpatient.treatments,
            surgeries = inpatient.surgeries,
            prev_diagnosis = inpatient.prev_diagnosis,
            prev_treatments = inpatient.prev_treatments,
            prev_surgeries = inpatient.prev_surgeries,
            # picture = inpatient.picture,
        )
        db.add(new_inpatient)
        db.commit()
        db.refresh(new_inpatient)
        return {
            "data": new_inpatient,
            "error": False,
            "message": f"New InPatient with id '{new_inpatient.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    inpatient = db.query(models.InPatient).filter(models.InPatient.id == id)
    if not inpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'InPatient with id {id} not found')
    else:
        inpatient.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"InPatient with id '{id}' has been successfully re-activated." 
        return res

def update(id, InPatient, db: Session):
    inpatient = db.query(models.InPatient).filter(models.InPatient.id == id)
    if not inpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'InPatient with id {id} not found')
    else:
        inpatient.update({
            "first_name" : InPatient.first_name,
            "middle_name" : InPatient.middle_name,
            "last_name" : InPatient.last_name,
            "suffix_name" : InPatient.suffix_name,
            "birth_date" : InPatient.birth_date,
            "gender" : InPatient.gender,
            "contact_no" : InPatient.contact_no,
            "email" : InPatient.email,
            "blood_type" : InPatient.blood_type,
            "diagnosis" : InPatient.diagnosis,
            "tests" : InPatient.tests,
            "treatments" : InPatient.treatments,
            "surgeries" : InPatient.surgeries,
            "prev_diagnosis" : InPatient.prev_diagnosis,
            "prev_treatments" : InPatient.prev_treatments,
            "prev_surgeries" : InPatient.prev_surgeries,
            # "picture" = InPatient.picture,
        })
        db.commit()
        return {
            "data": InPatient,
            "error": False,
            "message": f"InPatient with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    inpatient = db.query(models.InPatient).filter(models.InPatient.id == id)
    if not inpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'InPatient with id {id} not found')
    else:
        inpatient.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"InPatient with id = {id} has been successfully deleted." 
        return res