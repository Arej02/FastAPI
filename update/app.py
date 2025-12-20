from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated,Optional
from pathlib import Path
import json

base_url=Path.cwd().parent
file_path=base_url/"data"/"patients.json"

def load_data(url):
    with open(url,'r') as f:
        data=json.load(f)

    return data

def save_data(url,data):
    with open(url,'w') as f:
        json.dump(data,f)


class PatientSchema(BaseModel):
    id:Annotated[str,Field(...,title="Patient ID",description="Write the patient id",example="P0012")]
    name:Annotated[str,Field(...,title="Name of the patient",description="Write the name of the patient",example="Ravi")]
    city:Annotated[str,Field(...,title="City",description="Write the city of the patient",example="Hyderabad")]
    age:Annotated[int,Field(...,title="Age",description="Enter the age of person",example=22)]
    gender:Annotated[Literal["male","female","other"],Field(...,title="gender",description="Enter the gender of person",example='Male')]
    height:Annotated[float,Field(...,title="height",description="Enter the height of person in m",example=1.75)]
    weight:Annotated[float,Field(...,title="weight",description="Enter the weight of person in kg",example=72)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height*self.height),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif 18.5<=self.bmi<=24.9:
            return "Normal"
        elif 25<=self.bmi<=29.9:
            return "Overweight"
        else:
            return "Obese"

class UpdateSchema(BaseModel):  
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    height: Optional[float] = None
    weight: Optional[float] = None


app=FastAPI()

@app.get("/")
def home():
    return {
        'message':'Welcome to patient record system'
    }

@app.put("/home/{patient_id}")
def update_info(patient_id:str,update_info:UpdateSchema):

    # Check if the user id is present in the data:
    data=load_data(file_path)
    
    if patient_id  not in data:
        raise HTTPException(status_code=400,detail="Incorrect Patient ID")
    
    # Convert the updated into from pydantic object to a python dictionary for comparision with original data:
    update_info=update_info.model_dump(exclude_unset=True) # We only need values that is send by client
    existing_data=data[patient_id]

    # Update the information to the database:
    for key,value in update_info.items():
        existing_data[key]=value

    # Compute BMI and Verdict:
    existing_data['id']=patient_id
    pydantic_object=PatientSchema(**existing_data)

    existing_data=pydantic_object.model_dump(exclude='id')

    data[patient_id]=existing_data

    save_data(file_path,data)

    return JSONResponse(status_code=200,content={'message':'The data has been successfully updated'})




