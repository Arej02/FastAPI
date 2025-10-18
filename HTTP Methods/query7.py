'''Create an endpoint that takes a city and returns the average BMI of patients in that city — optionally filtered by gender.'''

from fastapi import FastAPI,HTTPException,Path,Query
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


@app.get("/patients/{city_name}")
def avg_bmi(city_name:str=Path(...,example='Hyderabad',description="Enter the city"),
            gender:str=Query(None,example="Male",description="Enter the gender")):
    
    data=load_data()

    counter=0
    total_bmi=0

    for patient in data.values():
        city=patient.get("city")

        if city.lower()==city_name.lower():
            bmi_value=patient.get("bmi",0)
            total_bmi+=bmi_value
            counter+=1

            

    if counter==0:
        logger.info("Ther was no such city")
        raise HTTPException(status_code=400,detail="No such city")
    

    avg=total_bmi/counter

    return {"city": city_name, "average_bmi": avg, "count": counter}



