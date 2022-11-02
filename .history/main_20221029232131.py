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

@app.get("/posts")
def get_posts():
