'''Practice Question: Filter Patient by ID and Check if Diagnosed with a Specific Disease

Create an endpoint that:
1. Accepts a patient ID as a path parameter.
2. Accepts a disease name (e.g., "Diabetes", "Hypertension") as a query parameter.
3. Returns the patient's details only if they are diagnosed with that disease.
4. If the patient is not found, return a 400 error.
5. If the disease does not match, return a 404 error.'''

from fastapi import FastAPI,HTTPException,Path,Query
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data



@app.get("/")
def home():
    return {"message": "Some query practise"}

@app.get("/patient/{patient_id}/filter")
def get_patient(patient_id:str=Path(...,description="Enter the patient id",example="P001"),condition:str=Query(...,description="Enter a condition",example="Obese")):

    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Invalid Input")
    
    patient=data[patient_id]

    if patient.get("verdict","").lower()==condition.lower():
        return patient
    else:
        raise HTTPException(status_code=404,detail="Disease not matched")




