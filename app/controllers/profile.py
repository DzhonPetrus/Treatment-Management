from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return {
        "data": profiles,
        "error": False,
        "message": "Profiles has been successfully retrieved."
    }

def get_one(id, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile with id {id} not found')
    return {
        "data": profile,
        "error": False,
        "message": f" Profile with id = {id} has been successfully retrieved."
    }

def create(profile, db: Session):
    new_profile = models.Profile(
        department = profile.department,
        position = profile.position,
        first_name = profile.first_name,
        middle_name = profile.middle_name,
        last_name = profile.last_name,
        suffix_name = profile.suffix_name,
        birth_date = profile.birth_date
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {
        "data": new_profile,
        "error": False,
        "message": f"New Profile with id '{new_profile.id}' has been successfully created."
    }

def reactivate(id, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile with id {id} not found')
    else:
        profile.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Profile with id '{id}' has been successfully re-activated." 
        return res

def update(id, Profile, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile with id {id} not found')
    else:
        profile.update({
            "department" : Profile.department,
            "position" : Profile.position,
            "first_name" : Profile.first_name,
            "middle_name" : Profile.middle_name,
            "last_name" : Profile.last_name,
            "suffix_name" : Profile.suffix_name,
            "birth_date" : Profile.birth_date,
            "is_active": Profile.is_active
        })
        db.commit()
        return {
            "data": Profile,
            "error": False,
            "message": f"Profile with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile with id {id} not found')
    else:
        profile.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"Profile with id = {id} has been successfully deleted." 
        return res