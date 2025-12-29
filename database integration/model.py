from sqlalchemy import Column,Integer,String
from database import Base

class Employee(Base):
    __tablename__="employees"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),index=True)
    email=Column(String(255),unique=True,index=True)