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
    
    image:Optional[str] = None

class UserOut(BaseModel):
    email: EmailStr
    clientid: Optional[int]
    devid:Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
class Business(BaseModel):
    name: str
    email: EmailStr
    username: str
    businessid: int
    tag:str
    isFeatured:bool
    created_at: datetime
    owner:UserOut

    class Config:
        orm_mode = True

class DevOut(BaseModel):
    email: EmailStr
    devid: int
    tag:str
    created_at: datetime

    class Config:
        orm_mode = True

# Our response schemas
class Post(PostBase):
    id:int
    created_at: datetime
    owner: DevOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
class PostUpdate(Post):
    pass

    class Config:
        orm_mode = True



# Users Base Schema

class ClientCreate(BaseModel):
    email: EmailStr
    password: str
    clientid: Optional[int]
    
class DevCreate(BaseModel):
    email: EmailStr
    password: str
    devid: Optional[int]


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
    postid: int
    dir: conint(le=1)# < = to 1
