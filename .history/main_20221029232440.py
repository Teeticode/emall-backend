from random import randrange
from turtle import title
from typing import Optional 
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    title:str
    desc: str
    price: int
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message":"Hello world"}

@app.get("/product")
def get_posts():
    return {"data"}

@app.post('/product')
def createProduct(prod:Product):
    prod_dict = prod.dict()
    prod_dict['id'] = randrange(0,100000)