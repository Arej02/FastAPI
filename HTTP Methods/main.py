from fastapi import FastAPI,HTTPException,Path,Query
import json
app=FastAPI()

#Load the data:
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

#Basic Home Page:
@app.get("/")
def home():
    return {'message':'Welcome to Patients Management System'}

#View all the data:
@app.get("/view")
def view():
    data=load_data()
    return data

#Path Parameter 1: Get Patient by Patient ID
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='ID of patient in the Database',example='P004')):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    else:
        return data[patient_id]

#Query Parameter 1: Sort by height, bmi or Weight
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
    

#Path and Query Parameter 1: Use path for age and gender for query

@app.get("/age/{age}")
def get_age(age:int=Path(...,description="Enter your age")):
    data=load_data()
    answer=[patient for patient in data.values() if patient.get("age","")==age]

    if not answer:
        raise HTTPException(status_code=400,detail="Invalid age")
    
    return answer

@app.get("/age")
def get_age_query(gender:str=Query(...,description="Enter male/female")):

    data=load_data()

    list=['male','female']
    if gender.lower() not in list:
        raise HTTPException(status_code=400,detail=f"Invalid input. Enter {list}")
    
    result=[patient for patient in data.values() if patient.get("gender").lower()==gender.lower() ]

    if not result:
        raise HTTPException(status_code=404,detail="Patient not available")
    
    return result


