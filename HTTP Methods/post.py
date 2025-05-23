from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json

app=FastAPI()

#Function to load the json file:
def load_data():
    with open ('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
#Pydantic Class
class Patient(BaseModel):
    id:Annotated[str,Field(...,description="Enter the patient ID",examples=['P001'])]
    name:Annotated[str,Field(...,description="Enter the patients name:")]
    city:Annotated[str,Field(...,description="Enter the city:")]
    age:Annotated[int,Field(...,gt=0,le=120,description="Enter the patients age:")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Enter the patients name:")]
    height:Annotated[float,Field(...,gt=0,description="Enter the patients height in m:")]
    weight:Annotated[float,Field(...,gt=0,description="Enter the patient weight in kg:")]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdit(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<24.9:
            return 'Normal'
        elif self.bmi<29.9:
            return 'Overweight'
        else:
            return 'Obese'



#Home Page:             
@app.get("/")
def home():
    return {'message':'Welcome to Patient Management System'}

#Patients route to view the patients record:
@app.get("/patients")
def view_record():
    data=load_data()
    return data

#To post the data:
@app.post("/create")
def create_patient(patient:Patient):

    #Load the data
    data=load_data()

    #Check if the Patient is already in the record
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patients already in record")
    
    #Convert the Patient datatype into dictionary
    data[patient.id]=patient.model_dump(exclude=['id'])

    #Save the data in the json file
    save_data(data)
    #Send a Response to the client
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})

