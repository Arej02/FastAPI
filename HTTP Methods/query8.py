'''Count Patients by Verdict
Create an endpoint that returns how many patients fall under each verdict category
(e.g., {"Underweight": 1, "Normal": 1, "Overweight": 2, "Obese": 2}).'''

from fastapi import FastAPI,HTTPException
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

@app.get("/patients/verdict")
def verdict_category():

    data=load_data()

    verdict={}

    for patient in data.values():
        category=patient.get("verdict")

        if category:
            verdict[category]=verdict.get(category,0)+1

    return verdict





