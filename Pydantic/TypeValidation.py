#pip install pydantic
from pydantic import BaseModel
from typing import List,Dict,Optional

#Using pydantic for type and data validation
class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool=False
    allergies: Optional[List[str]]=None #Optinal and default value is None
    contact_details:Dict[str,str]


patient_info={'name':'Arya','age':22,'weight':76,'married':False,'allergies':['dust','water'],'contact_details':{'email':'arya@gmail.com','phone':'4567898'}}
patient1=Patient(**patient_info) #Unpack the dictionary


def insert_patient_name(patient:Patient):
    print(patient.name)
    print(patient.age) 
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)


insert_patient_name(patient1)