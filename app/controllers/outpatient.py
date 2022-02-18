from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    outpatients = db.query(models.OutPatient).all() if is_active == '' else db.query(models.OutPatient).filter(models.OutPatient.is_active == is_active).all()
    return {
        "data": outpatients,
        "error": False,
        "message": "OutPatients has been successfully retrieved."
    }

def get_one(id, db: Session):
    outpatient = db.query(models.OutPatient).filter(models.OutPatient.id == id).first()
    if not outpatient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'OutPatient with id {id} not found')
    return {
        "data": outpatient,
        "error": False,
        "message": f" OutPatient with id = {id} has been successfully retrieved."
    }

def create(outpatient, db: Session):
    check = db.query(models.OutPatient).filter(models.OutPatient.email == outpatient.email)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'OutPatient with email {outpatient.email} already exist.')
    else:
        new_outpatient = models.OutPatient(
            first_name = outpatient.first_name,
            middle_name = outpatient.middle_name,
            last_name = outpatient.last_name,
            suffix_name = outpatient.suffix_name,
            birth_date = outpatient.birth_date,
            gender = outpatient.gender,
            contact_no = outpatient.contact_no,
            email = outpatient.email,
            blood_type = outpatient.blood_type,
            # picture = outpatient.picture,
        )
        db.add(new_outpatient)
        db.commit()
        db.refresh(new_outpatient)
        return {
            "data": new_outpatient,
            "error": False,
            "message": f"New OutPatient with id '{new_outpatient.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    outpatient = db.query(models.OutPatient).filter(models.OutPatient.id == id)
    if not outpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'OutPatient with id {id} not found')
    else:
        outpatient.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"OutPatient with id '{id}' has been successfully re-activated." 
        return res

def update(id, OutPatient, db: Session):
    outpatient = db.query(models.OutPatient).filter(models.OutPatient.id == id)
    if not outpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'OutPatient with id {id} not found')
    else:
        outpatient.update({
            "first_name" : OutPatient.first_name,
            "middle_name" : OutPatient.middle_name,
            "last_name" : OutPatient.last_name,
            "suffix_name" : OutPatient.suffix_name,
            "birth_date" : OutPatient.birth_date,
            "gender" : OutPatient.gender,
            "contact_no" : OutPatient.contact_no,
            "email" : OutPatient.email,
            "blood_type" : OutPatient.blood_type,
            # "picture" = OutPatient.picture,
        })
        db.commit()
        return {
            "data": OutPatient,
            "error": False,
            "message": f"OutPatient with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    outpatient = db.query(models.OutPatient).filter(models.OutPatient.id == id)
    if not outpatient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'OutPatient with id {id} not found')
    else:
        outpatient.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"OutPatient with id = {id} has been successfully deleted." 
        return res