from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
from pathlib import Path as path
import pickle
import pandas as pd



class Insurance(BaseModel):
    age:Annotated[int,Field(...,title="Age",description="Enter the age of the person",example=34,ge=0,le=120)]
    weight:Annotated[float,Field(...,title="Weight",description="Enter the weight of the person in kg",example=45,ge=0)] 
    height:Annotated[float,Field(...,title="Height",description="Enter the height of the person in m",example=1.70,ge=0)]
    income_lpa:Annotated[float,Field(...,title="Income",description="Enter the salary of the person in lpa",example=6.5,ge=0)]
    smoker:Annotated[bool,Field(...,title="Somker",description="Enter True if the person smokes",example=True)]
    city:Annotated[Literal['Jaipur', 'Chennai', 'Indore', 'Mumbai', 'Kota', 'Hyderabad','Delhi', 'Chandigarh', 'Pune', 'Kolkata', 'Lucknow', 'Gaya','Jalandhar', 'Mysore', 'Bangalore'],Field(...,title="City",description="Enter the city of the person",example="Hyderabad")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'],Field(...,title="Occupation",description="Enter the occupation of the person",example='government_job')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height*self.height),2)
        return bmi
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age<0:
            return "Child"
        elif 20<=self.age<40:
            return "Young Adult"
        elif 40<=self.age<60:
            return "Adult"
        else:
            return "Senior"
        
    @computed_field
    @property
    def city_tier(self)->int:
        tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2_cities = [
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3



    @computed_field
    @property
    def risk_category(self)->str:
        if self.smoker==True and self.bmi>29.9:
            return "High"
        elif self.smoker==True and 24.9<=self.bmi<29.9:
            return "Medium"
        elif self.smoker==False and self.bmi>25:
            return "Medium"
        else:
            return "Low"

        

file_path=path.cwd()/"model.pkl"
def load_model():
    with open(file_path,"rb") as f:
        data=pickle.load(f)

    return data

app=FastAPI()

@app.get("/")
def home():
    return {
        "message":"Welcome to our insurance company"
    }

@app.post("/home/predict")
def make_prediction(data:Insurance):

    input_df=pd.DataFrame([
        {
            "bmi":data.bmi,
            "age_group":data.age_group,
            "occupation":data.occupation,
            "city_tier":data.city_tier,
            "income_lpa":data.income_lpa,
            "risk_category":data.risk_category
        }
    ])
    model=load_model()
    prediction=model.predict(input_df)[0]

    return JSONResponse(status_code=200,content={'predicted_category':prediction})







