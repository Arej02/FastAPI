'''Create an endpoint that returns all patients in a given city who are also within a specific verdict category.'''

from fastapi import FastAPI,HTTPException,Path
import logging
import json

app=FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger=logging.getLogger('Patients Verdict Count')

def load_data():
    try:
        with open('patients.json','r') as f:
            data=json.load(f)
            logger.info("File opened")
            return data
    except FileNotFoundError as e:
        logger.info("Database doesnot exist")
        raise HTTPException(status_code=400,detail="Database doesnot exist")

@app.get("/")
def home():
    return {'message':'Welcome to patients management system'}

@app.get("/patients/{city_name}/{verdict_category}")
def city_verdict(
    city_name:str=Path(...,example="Hyderabad",description="Enter the city"),
    verdict_category:str=Path(...,example="Obese",description="Enter the verdict category")
):
    data=load_data()
    matched_patients=[]

    for patient in data.values():
        city=patient.get("city","")
        verdict=patient.get("verdict","")
        if city.lower()==city_name.lower() and verdict.lower()==verdict_category.lower():
            matched_patients.append(patient)

    if not matched_patients:
        raise HTTPException(status_code=404,detail="No patient from {city_name} of verdict {verdic_category} found")

    return {
        "city_name":city_name,
        "verdict_category":verdict_category,
        "count":len(matched_patients),
        "patients":matched_patients
    }
        







