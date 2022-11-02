from email import message
from .. import oauth2
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
    new_customer = models.Users(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@router.post('/business', status_code=status.HTTP_201_CREATED, response_model=schemas.BusinessOut)
def create_user(biz: schemas.BusinessCreate,
curr_user: int=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request")
    biz.businessid = randrange(0, 50000000)
    biz.userid = curr_user.userid
    # hash the password
    hashed_psd = utils.hash(biz.password)
    queryd= db.query(models.Business).filter((models.Business.email ==biz.email)).first()
    
    if queryd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credintials Error"
        )

    biz.password = hashed_psd
    new_biz = models.Business(**biz.dict())
    db.add(new_biz)
    db.commit()
    db.refresh(new_biz)

    return new_biz



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
