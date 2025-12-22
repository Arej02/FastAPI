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


app=FastAPI()

@app.get("/")
def home():
    return {
        'message':'Welcome to patient record system'
    }

@app.delete("/home/{patient_id}")
def delete_info(patient_id:str):

    data=load_data(file_path)

    if patient_id not in data:
        raise HTTPException(status_code=400,detail="The patient is not in the database")

    del data[patient_id]

    save_data(file_path,data)

    return JSONResponse(status_code=200,content={'message':'The record has been deleted'})






