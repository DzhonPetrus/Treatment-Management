from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return profiles

def get_one(id, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile with id {id} not found')
    return profile

def create(profile, db: Session):
    new_profile = models.Profile(
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
    return new_profile