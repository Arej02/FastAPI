from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import Insurance
from model.predict import load_model,predict_output



app=FastAPI()

@app.get("/")
def home():
    return {
        "message":"Welcome to our insurance company"
    }
@app.get("/health")
def health_check():
    return{
        'status':'OK'
    }

@app.post("/home/predict")
def make_prediction(data:Insurance):

    input_df={
            "bmi":data.bmi,
            "age_group":data.age_group,
            "occupation":data.occupation,
            "city_tier":data.city_tier,
            "income_lpa":data.income_lpa,
            "risk_category":data.risk_category
        }

    prediction=predict_output(input_df)

    return JSONResponse(status_code=200,content={'predicted_category':prediction})







