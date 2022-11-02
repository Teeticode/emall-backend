from msilib import schema
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
router = APIRouter(
    tags=['Authentication'],
    prefix="/auth"
)

@router.post('/customer/login', response_model=schemas.Token)
def login(user_cr: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    
    log_user = db.query(models.Users).filter(models.Users.email == user_cr.username).first()
    if not log_user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials')
    if not utils.verify_psd(user_cr.password, log_user.password):
       raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f'Invalid Credentials')

    # create a token
    access_token = oauth2.create_access_token(data = {"userid": log_user.userid})
    # return token
    return{'token':access_token, "token_type": "Bearer"}

@router.post('/business/login', response_model=schemas.Token)
def login(user_cr: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    
    log_user = db.query(models.Business).filter(models.Business.email == user_cr.username).first()
    if not log_user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials')
    if not utils.verify_psd(user_cr.password, log_user.password):
       raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f'Invalid Credentials')

    # create a token
    access_token = oauth2.create_access_token(data = {"userid": log_user.businessid})
    # return token
    return{'token':access_token, "token_type": "Bearer"}
