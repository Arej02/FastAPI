'''Filter by BMI Range
Query parameters: min_bmi, max_bmi
Return all patients within the BMI range.
If no patients match, return 404.'''

from fastapi import FastAPI,Query,HTTPException
import json

app=FastAPI()

def load_data():
    with open ('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def home():
    return {'message':'Welcome to Patient Management System'}

@app.get("/patients")
def bmi_range(min_bmi:float=Query(...,description="Enter the minimum bmi"),
              max_bmi:float=Query(...,description="Enter the maximum bmi")):
    
    #Load the data:
    data=load_data()

    #Find the bmi range in data:
    result=[patient for patient in data.values()
            if min_bmi<=patient.get("bmi",0)<=max_bmi]
    
    if not result:
        raise HTTPException(status_code=404,detail="No patients found")
    
    return result