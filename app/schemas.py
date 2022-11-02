from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from tokenize import String
from typing import Optional

class UserOut(BaseModel):
    username: str
    email: EmailStr
    userid: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
class Business(BaseModel):
    name: str
    email: EmailStr
    businessid: int
    tag:str
    isFeatured:bool = False
    created_at: Optional[datetime]
    
    userid: Optional[str]
    owner:UserOut

    class Config:
        orm_mode = True
# schemas
class ProductBase(BaseModel):
    title: str
    desc: str
    published: bool=True
    isFeatured: bool=False
    rating: Optional[int] = None
    numReviews: Optional[int] = None
    productid: Optional[int]
    businessid: Optional[int]
    image:Optional[str] = None
    owner: Optional[Business] 

class CreateBase(ProductBase):
    pass

class UpdateBase(BaseModel):
    title: str
    desc: str
    published: bool=True
    isFeatured: bool=False
    rating: Optional[int] = None
    numReviews: Optional[int] = None
    image: Optional[str] = None
    




# Our response schemas
class Product(ProductBase):
    id:int
    created_at: datetime
    owner: Business

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    Product: Product
    votes: int

    class Config:
        orm_mode = True
class ProductUpdate(Product):
    pass

    class Config:
        orm_mode = True



# Users Base Schema

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    userid: Optional[str]

class BusinessCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    businessid: Optional[str]
    userid: Optional[str]
    
class BusinessOut(BaseModel):
    name: str
    email: EmailStr
    password: str
    businessid: str
    userid: Optional[str]
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# Vote schema

class Vote(BaseModel):
    productid: str
    dir: conint(le=1)# < = to 1
