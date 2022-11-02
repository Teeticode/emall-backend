from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Product(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable = false)
    title = Column(String, nullable = false)
    desc = Column(String, nullable = false)
    published = Column(Boolean, default=True)