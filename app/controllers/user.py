from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models

def get_all(db: Session, is_active = ''):
    users = db.query(models.User).all() if is_active == '' else db.query(models.User).filter(models.User.is_active == is_active).all()
    return {
        "data": users,
        "error": False,
        "message": "Users has been successfully retrieved."
    }

def get_one(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return {
        "data": user,
        "error": False,
        "message": f" User with id = {id} has been successfully retrieved."
    }

def create(user, db: Session):
    check = db.query(models.User).filter(models.User.email == user.email)
    if check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'User with name {user.name} already exist.')
    else:
        new_user = models.User(
            email = user.email,
            password = user.password,
            user_profile_id = user.user_profile_id,
            user_type = user.user_type
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "data": new_user,
            "error": False,
            "message": f"New User with id '{new_user.id}' has been successfully created."
        }

def reactivate(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    else:
        user.update({
            "is_active": "ACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"User with id '{id}' has been successfully re-activated." 
        return res

def update(id, User, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    else:
        user.update({
            "email": User.email,
            "password": User.password,
            "user_type": User.user_type,
            "user_profile_id": User.user_profile_id,
            "is_active": User.is_active
        })
        db.commit()
        return {
            "data": User,
            "error": False,
            "message": f"User with id '{id}' has been successfully updated."
        }

def destroy(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    else:
        user.update({
            "is_active": "INACTIVE"
        })
        db.commit()
        res = get_one(id, db)
        res["message"] = f"User with id = {id} has been successfully deleted." 
        return res