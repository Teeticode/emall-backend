from math import prod
from random import randrange
from turtle import title
from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routers import product, user
from pydantic import BaseModel
from typing import Optional


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(product.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Hello world"}



