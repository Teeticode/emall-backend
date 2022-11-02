from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable = False)
    desc = Column(String, nullable = False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), 
    nullable=False, server_default=text('NOW()'))
    productid = Column(BigInteger, nullable=False, unique=True)
    image = Column(String, nullable=False, server_default="null")
    businessid =  Column(String, 
            ForeignKey("business.businessid", ondelete="CASCADE"), nullable=False)
    isFeatured = Column(Boolean, default=False)
    owner = relationship("Business")

class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable = False, unique=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    businessid = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                nullable=False, server_default=text('NOW()'))
    tag = Column(String, nullable=False, server_default='business')
    isFeatured = Column(Boolean, default=False)
    userid =  Column(String, 
            ForeignKey("users.userid", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    userid = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                nullable=False, server_default=text('NOW()'))
    tag = Column(String, nullable=False, server_default='users')

class Vote(Base):
    __tablename__ = 'votes'
    userid = Column(String, ForeignKey('users.userid', ondelete="CASCADE"), primary_key=True)
    productid = Column(String, ForeignKey('products.productid', ondelete="CASCADE"), primary_key=True)