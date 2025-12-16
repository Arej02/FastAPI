from pydantic import BaseModel,Field,computed_field
from typing import List,Literal,Annotated
from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import json

base_path=Path(__file__).parent.parent
file_path=base_path/"data"/"patients.json"

def load_data(url):
    with open(url,'r') as f:
        data=json.load(f)
    return data

def save_data(url,data):
    with open(url,'w') as f:
        json.dump(data,f)


class Patient(BaseModel):
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
    return {'message':"Welcome to patient record system"}

@app.post("/create")
def add_record(patient:Patient):

    data=load_data(file_path)

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Duplicate patient ID")
    
    data[patient.id]=patient.model_dump(exclude=["id"]) # Converts the pydantic object to python dicionary

    save_data(file_path,data)

    return JSONResponse(status_code=201,content={"message":"Patient added to the database"})
