from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict


class Student(BaseModel):
    name:str=Field(...,max_length=50)
    email:EmailStr
    linkedin:AnyUrl
    contact:int
    weight:float
    marks:Dict[str,int]


def insert_data(student:Student):
    print(student.name)
    print(student.marks)


std1=Student(
    name='Arya',
    email='khadkaarya15@gmail.com',
    linkedin='https://www.linkedin.com/in/arya00/',
    contact=430034022,
    weight=75.8,
    marks={'DSA':82,'Data Science':87,'Statistics':90,'Linear Algebra':79}
)

insert_data(std1)