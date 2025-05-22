'''2. Check if Patient is Above a Certain Age
Path parameter: patient_id
Query parameter: min_age
Return patient if age ≥ min_age.
If patient not found, return 400.
If age is below the given, return 404.
'''

from fastapi import FastAPI,Path,Query,HTTPException
import json

app=FastAPI()

def load_data():
    with open ('patients.json','r') as f:
        data=json.load(f)
    return data


@app.get("/")
def home():
    return {'message':'Hello'}


@app.get("/patients/{patient_id}")
def patient_by_age(patient_id:str=Path(...,description="Enter the patient Id"),
                   min_age:int=Query(...,description="Enter the age")):
    
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient not found")
    
    patient=data[patient_id]

    result=[val for val in patient.values() if patient.get("age",0)>=min_age]

    if not result:
        raise HTTPException(status_code=404,detail="The age requirement is not met")

    return result