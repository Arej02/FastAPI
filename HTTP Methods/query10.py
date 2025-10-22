'''Create an endpoint that returns a list of unique cities found in the dataset.'''

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


@app.get("/unique_city")
def city_names():

    data=load_data()
    city=[]

    for patients in data.values():
        city_name=patients.get("city",'')
        if city_name not in city:
            city.append(city_name)

    return {
        "city":city
            }
