from random import randrange
from turtle import title
from typing import Optional 
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

products = []
class Product(BaseModel):
    title:str
    desc: str
    price: int
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message":"Hello world"}

@app.get("/products")
def get_posts():
    return {"data"}

@app.post('/products')
def createProduct(prod:Product):
    prod_dict = prod.dict()
    prod_dict['id'] = randrange(0,100000)
    products.append(prod_dict)
    return {"data": prod_dict}
