from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable = False)
    desc = Column(String, nullable = False)
    published = Column(Boolean, default=True)