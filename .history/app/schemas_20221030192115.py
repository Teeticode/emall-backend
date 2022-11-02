from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from tokenize import String
from typing import Optional

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
    owner: Optional[str] 

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
    
    image:Optional[str] = None

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
    isFeatured:bool
    created_at: Optional[datetime]
    productids: Optional[str]
    products: ProductBase
    owner:UserOut

    class Config:
        orm_mode = True


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
class PostUpdate(Product):
    pass

    class Config:
        orm_mode = True



# Users Base Schema

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    userid: Optional[int]
    


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
