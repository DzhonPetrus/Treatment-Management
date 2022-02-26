from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from .. import models

def get_all(db: Session, is_active = ''):
    surgeries = db.query(models.Surgery).all() if is_active == '' else db.query(models.Surgery).filter(models.Surgery.is_active == is_active).all()
    # return surgeries
    return {
        "data": surgeries,
        "error": False,
        "message": "Surgeries has been successfully retrieved."
    }

def get_one(id, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id).first()
    if not surgery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    return {
        "data": surgery,
        "error": False,
        "message": f" Surgery with id = {id} has been successfully retrieved."
    }

def create(surgery, db: Session):
    print(surgery)
    _surgery_no = 'SN-' + (str(uuid4()).split('-')[0]).upper()
    new_surgery = models.Surgery(
        surgery_no = _surgery_no,
        inpatient_id = surgery.inpatient_id,
        surgery_service_id = surgery.surgery_service_id,
        head_surgeon_id = surgery.head_surgeon_id,
        description = surgery.description,
        room = surgery.room,
        start_time = surgery.start_time,
        status = surgery.status,
        is_active = surgery.is_active
    )

    db.add(new_surgery)
    db.flush()
    db.commit()
    # db.refresh(new_surgery)
    print(new_surgery.id)

    in_charge = surgery.in_charge
    
    if(in_charge.find(',') != -1):
        in_charge = in_charge.split(',')

    print(in_charge)

    in_charges = []
    for _id in in_charge:
        in_charges.append(models.SurgeryInCharge(in_charge_id=_id, surgery_id=new_surgery.id))
    
    # print(in_charges)
    # new_surgery.in_charges = in_charges

    db.add_all(in_charges)
    db.commit()
    db.refresh(new_surgery)
    return {
        "data": new_surgery,
        "error": False,
        "message": f"New Surgery with id '{new_surgery.id}' has been successfully created."
    }

def cancel(id, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id)
    if not surgery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    else:
        surgery.update({
            "status": "CANCELLED"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Surgery with id '{id}' has been successfully cancelled." 
        return res

def reactivate(id, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id)
    if not surgery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    else:
        surgery.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Surgery with id '{id}' has been successfully re-activated." 
        return res

def update(id, Surgery, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id)
    if not surgery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    else:
        surgery.update({
            "surgery_no" : Surgery.surgery_no,
            "inpatient_id" : Surgery.inpatient_id,
            "surgery_service_id" : Surgery.surgery_service_id,
            "head_surgeon_id" : Surgery.head_surgeon_id,
            "description" : Surgery.description,
            "room" : Surgery.room,
            "start_time" : Surgery.start_time,
            "end_time" : Surgery.end_time,
            "status" : Surgery.status,
            "is_active" : Surgery.is_active
        })
        db.commit()
        return {
            "data": Surgery,
            "error": False,
            "message": f"Surgery with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    surgery = db.query(models.Surgery).filter(models.Surgery.id == id)
    if not surgery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Surgery with id {id} not found')
    else:
        surgery.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Surgery with id = {id} has been successfully deleted." 
        return res