from fastapi import FastAPI,HTTPException,Path,Query
import json
app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def home():
    return {'message':'Welcome to Patients Management System'}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='ID of patient in the Database',example='P004')):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    else:
        return data[patient_id]

@app.get("/sort")
def sort_values(sort_by:str=Query(...,description="Sort by height,bmi,Weight"),order_by:str=Query('asc',description="Order by asc or desc")):

    data=load_data()
    valid_inputs=['height','weight','bmi']

    if sort_by not in valid_inputs:
        raise HTTPException(status_code=400,detail=f"Invalid input.Enter from {valid_inputs}")
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"Invalid input")
    
    sort= True if order_by=='desc' else False

    result=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort)

    return result
    

