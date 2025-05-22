from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import Annotated

#Field is allowing you to also put constraints,put default values and provide some meta-data
class Patient(BaseModel):
    name:Annotated[str,Field(max_length=50,title="Name of the patient",examples=['Arya'])]
    email:EmailStr
    LinkedIn:AnyUrl
    age:Annotated[int,Field(gt=0,lt=120,title="Age of the patients")]
    weight:Annotated[float,Field(gt=0,title="Enter your weight")]
    married:Annotated[bool,Field(default='Not Married',description="Is the patient married or not?" )]

patient_info={'name':'Arya','email':'arya@gmail.com','LinkedIn':'https://www.linkedin.com/in/arya-raj-khadka-08a43531a/','age':22,'weight':76}
patient1=Patient(**patient_info) #Unpack the dictionary


def insert_patient_name(patient:Patient):
    print(patient.name)
    print(patient.age) 
    print(patient.weight)
    print(patient.married)



insert_patient_name(patient1)