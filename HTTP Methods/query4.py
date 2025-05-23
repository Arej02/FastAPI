'''7. Find Patients with Same Age
Path parameter: patient_id
Find and return all patients with the same age as the given patient.'''

from fastapi import FastAPI,Path,Query,HTTPException
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def home():
    return {'message':'Welcome to the home page'}

@app.get("/patients/{patient_id}")
def similar_age(patient_id:str=Path(...,description="Enter the patiet id",example="P001")):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient Not Found")
    
    target_age=data[patient_id].get("age",None)

    result=[]
    for pid,patient in data.items():
        if pid!=patient_id and patient.get("age")==target_age:
            result.append(patient)

    if not result:
        raise HTTPException(status_code=404, detail="No other patients found with the same age")
    
    return {
        "patient_id": patient_id,
        "age": target_age,
        "similar_age_patients": result
    }
    



