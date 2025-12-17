from fastapi import FastAPI
from typing import List,Annotated,Optional,Dict
from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator

# Nested Model
class Address(BaseModel):
    city:str
    state:str
    postal_code:int

class Person(BaseModel):
    name:Annotated[str,Field(title="Name",description="Enter the name of the person",examples=["John","Sita"])] 
    age:Annotated[int,Field(title="Age",description="Enter the age of the person",ge=0,le=120)]
    married:Annotated[bool,Field(default=False,title="Married",description="Enter your maritial status")]
    address:Address

add={'city':'Kathmandu','state':'Bagmati','postal_code':12000}
add1=Address(**add)

person={'name':'Ram','age':34,'married':True,'address':add1}
person1=Person(**person)

print(person1.name)
print(person1.address.city)

# Seralization:

temp=person1.model_dump(exclude=['married']) # Converts into python dictionary
print(temp)
