from pydantic_model import DevicesSchema
from fastapi import FastAPI,Path,Query,HTTPException
from pathlib import Path as path
import json

base_path=path.cwd().parent
file_path=base_path/"data"/"electronics.json"

def load_data(url):
    with open(url,'r') as f:
        data=json.load(f)
    return data

app=FastAPI()

@app.get("/")
def home():
    return {
        'message':"Welcome to Elecronics Database"
        }

@app.get("/products")
def display():
    data=load_data(file_path)
    return {
        'data':data
    }

@app.get("/products/{category}")
def smart_filer(
    category:str=Path(
        ...,description="Enter the category:(smartphone,laptop,headphones,tablet)",
        example="laptop"),
    min_rating:float | None = Query(
        None,
        description="Enter the minimum rating",
        ge=0,le=5),
    max_rating:float | None= Query(
        None,
        description="Enter the maximum rating",
        ge=0,le=5)
        ):
    
    if category.strip().lower() not in ["smartphone","laptop","headphones","tablet"]:
        raise HTTPException(status_code=400,detail="The category type not found.")
    
    data=load_data(file_path)

    category=category.strip().lower()

    result=[]
    for key,value in data.items():

        if value.get("category") != category:
            continue

        if min_rating is not None and value.get("rating",0)<min_rating:
            continue

        if max_rating is not None and value.get("rating",0)>max_rating:
            continue

        result.append({key:value})
 

    return {
        'count':len(result),
        'devices':result

    }


