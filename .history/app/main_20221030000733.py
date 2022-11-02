from random import randrange
from turtle import title
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import product


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    return {"data":products}

@app.post('/products', status_code = status.HTTP_201_CREATED)
def createProduct(prod:Product):
    prod_dict = prod.dict()
    prod_dict['id'] = randrange(0,100000)
    products.append(prod_dict)
    return {"data": prod_dict}

