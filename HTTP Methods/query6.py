'''Find the Youngest or Oldest Patient:

Create an endpoint that returns either the youngest or oldest patient based on a given parameter (e.g., "mode=youngest" or "mode=oldest").
Return 400 if the mode value is invalid.'''

from fastapi import FastAPI,HTTPException,Query
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger=logging.getLogger("Youngest/Oldest Patients")
def load_data():
    try:
        with open('patients.json') as f:
            data=json.load(f)
            logger.info("Database opened successfully")
            return data
    except FileNotFoundError as e:
        logger.info("Database does not exist")
        raise HTTPException(status_code=400,detail="Database does not exist")
    
app=FastAPI()

@app.get("/")
def home():
    return {'message':'Welcome to home page'}

@app.get("/patients")
def patient_type(
    mode:str=Query(...,description="Do you want the youngest or oldest patient",example="youngest/oldest")):

    data=load_data()
    
    if mode.lower() not in ['youngest','oldest']:
        raise HTTPException(status_code=400,detail="Enter the correct option")
    
    ages=[patients["age"] for patients in data.values() if "age" in patients]
    if not ages:
        raise HTTPException(status_code=404, detail="No age data found")

    youngest=min(ages)
    oldest=max(ages)

    if mode.lower()=="yongest":
        target=[patients for patients in data.values() if patients.get("age")==youngest]
    else:
        target=[patients for patients in data.values() if patients.get("age")==oldest]

    return target
    



    



