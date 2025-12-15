from fastapi import FastAPI
from typing import List,Annotated,Optional,Dict
from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator

class Patient(BaseModel):
    name:Annotated[str,Field(title="Name",description="Enter the name of the person",examples=["John","Sita"])] 
    age:Annotated[int,Field(title="Age",description="Enter the age of the person",ge=0,le=120)]
    married:Annotated[bool,Field(default=False,title="Married",description="Enter your maritial status")] 
    allergies:List[str]
    email:EmailStr
    linkedin:AnyUrl
    contact:Dict[str,str]

    # Check if the user is a student in Adelaide (@student.adelaide.edu.au):
    @field_validator('email') # Validator in the field of email 
    @classmethod

    def check_student(cls,value):
        
        email_end=value.split("@")[-1]
        if email_end!="student.adelaide.edu.au":
            raise ValueError("You must be a student based in adelaide")
        
        return value
    
    @model_validator(mode='after')

    def check_emergency_number(model):
        if model.age<18 and "emergency_number" not in model.contact:
            raise ValueError("People under 18 should have emergency number")
        
        return model


def insert_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.email)
    print(patient.allergies)
    print(patient.contact)

patient={
    "name":"Ram",
    "age":13,
    "allergies":["cough","cold","dust"],
    "email":"ram15@student.adelaide.edu.au",
    "linkedin":"https://www.linkedin.com/in/arya00/",
    "contact":{"phone_number":"839749283","emergency_number":"37904732890"}
    }

patient1=Patient(**patient)
insert_data(patient1)


