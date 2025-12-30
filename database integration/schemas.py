from pydantic import BaseModel,EmailStr
from typing import Optional


class Employee(BaseModel):
    name:str
    email:str


class CreateEmployee(Employee):
    email:Optional[EmailStr]

class UpdateEmployee(Employee):
    pass


class OutputEmployee(Employee):
    id:int

    class Config:
        orm_mode=True