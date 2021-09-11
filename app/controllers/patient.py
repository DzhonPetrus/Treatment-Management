from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    patients = db.query(models.Patient).all() if is_active == '' else db.query(models.Patient).filter(models.Patient.is_active == is_active)
    return {
        "data": patients,
        "error": False,
        "message": "Patients has been successfully retrieved."
    }

def get_one(id, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Patient with id {id} not found')
    return {
        "data": patient,
        "error": False,
        "message": f" Patient with id = {id} has been successfully retrieved."
    }

def create(patient, db: Session):
    check = db.query(models.Patient).filter(models.Patient.email == patient.email)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Patient with email {patient.email} already exist.')
    else:
        new_patient = models.Patient(
            type = patient.type,
            first_name = patient.first_name,
            middle_name = patient.middle_name,
            last_name = patient.last_name,
            suffix_name = patient.suffix_name,
            birth_date = patient.birth_date,
            gender = patient.gender,
            contact_no = patient.contact_no,
            email = patient.email,
            blood_type = patient.blood_type,
            # picture = patient.picture,
        )
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return {
            "data": new_patient,
            "error": False,
            "message": f"New Patient with id '{new_patient.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id)
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Patient with id {id} not found')
    else:
        patient.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Patient with id '{id}' has been successfully re-activated." 
        return res

def update(id, Patient, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id)
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Patient with id {id} not found')
    else:
        patient.update({
            "type" : Patient.type,
            "first_name" : Patient.first_name,
            "middle_name" : Patient.middle_name,
            "last_name" : Patient.last_name,
            "suffix_name" : Patient.suffix_name,
            "birth_date" : Patient.birth_date,
            "gender" : Patient.gender,
            "contact_no" : Patient.contact_no,
            "email" : Patient.email,
            "blood_type" : Patient.blood_type,
            # "picture" = Patient.picture,
        })
        db.commit()
        return {
            "data": Patient,
            "error": False,
            "message": f"Patient with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id)
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Patient with id {id} not found')
    else:
        patient.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Patient with id = {id} has been successfully deleted." 
        return res