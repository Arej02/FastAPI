from pydantic import BaseModel,Field
from typing import Annotated

class Employee(BaseModel):
    id:Annotated[int,Field(...,description="ID of the employee",examples=[12])]
    name:Annotated[str,Field(...,description="Name of the employee",examples=["Arya"])]
    department:Annotated[str,Field(...,description="Department of the employee",examples=["Marketing"])]
    age:Annotated[int,Field(...,description="Age of the employee",examples=[25],ge=0,le=120)]
