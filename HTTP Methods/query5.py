'''9. Compare Two Patients by BMI
Path parameters: patient_id1, patient_id2
Return which patient has higher BMI.
400 if either patient not found.'''

from fastapi import FastAPI,Path,HTTPException
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def home():
    return {'message':'Welcome to BMI Comparision of patients'}

@app.get("/compareBMI/{patient_id1}/{patient_id2}")
def compareBMI(patient_id1:str=Path(...,description="Enter the first patient ID",example="P001"),
               patient_id2:str=Path(...,description="Enter the second patient ID",example="P002")):
    
    data=load_data()

    if patient_id1 not in data:
        raise HTTPException(status_code=400,detail="Patient 1 not found")
    if patient_id2 not in data:
        raise HTTPException(status_code=400,detail="Patient 2 not found")
    
    patient1=data[patient_id1]
    patient2=data[patient_id2]

    bmi1=patient1.get("bmi",0)
    bmi2=patient2.get("bmi",0)

    if bmi1 > bmi2:
        return {"higher_bmi_patient": patient_id1, "bmi": bmi1}
    elif bmi2 > bmi1:
        return {"higher_bmi_patient": patient_id2, "bmi": bmi2}
    else:
        return {"message": "Both patients have the same BMI", "bmi": bmi1}