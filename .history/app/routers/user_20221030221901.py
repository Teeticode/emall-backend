from email import message
from fastapi import (APIRouter,
 HTTPException, status, Depends)
from random import randrange
from typing import List

from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# Create user
@router.post('/customers', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(customer: schemas.UserCreate, db: Session = Depends(get_db)):
    customer.userid = randrange(0, 50000000)
    # hash the password
    hashed_psd = utils.hash(customer.password)
    queryc= db.query(models.Users).filter((models.Users.email == customer.email)).first()
    
    if queryc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="try again. Something went wrong"
        )

    customer.password = hashed_psd
    new_customer = models.Client(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@router.post('/dev', status_code=status.HTTP_201_CREATED, response_model=schemas.DevOut)
def create_user(dev: schemas.DevCreate, db: Session = Depends(get_db)):
    dev.devid = randrange(0, 50000000)
    # hash the password
    hashed_psd = utils.hash(dev.password)
    queryd= db.query(models.Developer).filter((models.Developer.email ==dev.email)).first()
    
    if queryd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credintials Error"
        )

    dev.password = hashed_psd
    new_user = models.Developer(**dev.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# get all users



@router.get('/dev', response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.Developer).all()
    return users

@router.get('/client', response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.Client).all()
    return users

# get individual user

@router.get('/client/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Client).filter(models.Client.clientid == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user

@router.get('/dev/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Developer).filter(models.Developer.devid == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user
