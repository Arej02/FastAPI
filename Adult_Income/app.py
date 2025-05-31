from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Annotated,Literal
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8501",  
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Import the ML model:
with open('model.pkl','rb') as f:
    model=pickle.load(f)

with open('label_encoder.pkl','rb') as f:
    label=pickle.load(f)
  

#Pydantic Model:
class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,le=120,description="Enter the age")]

    workclass:Annotated[Literal['Government','Private','Unemployed'],Field(...,description="Enter your workclass")]

    educational_num:Annotated[int,Field(gt=0,le=18,description="Enter your education number",alias='educational-num')] 

    marital_status:Annotated[Literal['Divorced','Single','Married','Widow'],Field(...,description="Enter you marriage status")] 

    occupation:Annotated[Literal['Management','Professional','Services','Manual Labor','Protective Services','Armed Forces','Other'],Field(...,description="Enter your occupation")]

    relationship:Annotated[Literal['Own-child', 'Husband', 'Not-in-family', 'Unmarried', 'Wife','Other-relative'],Field(...,description="Enter your relationship")] 

    race:Annotated[Literal['Black', 'White', 'Asian-Pac-Islander', 'Other','Amer-Indian-Eskimo'],Field(...,description="Enter your race")]

    gender:Annotated[Literal['Male','Female'],Field(...,description="Enter your gender")]

    capital_gain:Annotated[float,Field(description="Enter your capital gain",alias='capital-gain')] 

    capital_loss:Annotated[float,Field(description="Enter your capital loss",alias='capital-loss')] 

    hours_per_week:Annotated[int,Field(description="Enter your hours worked",alias='hours-per-week')] 

    native_country: Annotated[Literal['US','Non US'],Field(...,description="Enter your country",alias='native-country')] 

@app.post("/predict")
def predict_income(data:UserInput):

    #Convert input data into dataframe:
    input_df = pd.DataFrame([{
        'age': data.age,
        'workclass': data.workclass,
        'educational-num': data.educational_num,
        'marital-status': data.marital_status,
        'occupation': data.occupation,
        'relationship': data.relationship,
        'race': data.race,
        'gender': data.gender,
        'capital-gain': data.capital_gain,
        'capital-loss': data.capital_loss,
        'hours-per-week': data.hours_per_week,
        'native-country': data.native_country
    }])


    #Prediction:
    prediction=model.predict(input_df)

    #Convert Prediction to readable
    prediction_label = label.inverse_transform([prediction[0]])[0]


    return {
        "predicted_category": prediction_label
    }

