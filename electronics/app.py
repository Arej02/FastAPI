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

@app.get("/stock")
def get_stock(threshold:int | None =Query(
    None,description="Enter the max number of stocks you want:")):

    data=load_data(file_path)

    result=[]

    for data_id,data_items in data.items():
        stock=data_items.get("stock",0)
        if stock==0 or (threshold is not None and data_items.get("stock")<threshold): 
            result.append({data_id:data_items})

    return {
        "count":len(result),
        "devices":result
    }

@app.get("/compare/{brand1}/{brand2}") 
def compare_brand(
    brand1:str=Path(
        ...,title="Brand 1",
        description="Enter the first brand",example="Dell"),
    brand2:str=Path(
        ...,title="Brand 2",
        description="Enter the second brand",example="Apple"
    )):

    data=load_data(file_path)
    allowed_brands=['apple','samsung','dell','sony']
    brand1=brand1.strip().lower()
    brand2=brand2.strip().lower()

    if brand1 not in allowed_brands or brand2 not in allowed_brands:
        raise HTTPException(status_code=404, detail="Brand not found")

    stats={
        brand1:{"price":[],"rating":[]},
        brand2:{"price":[],"rating":[]}
    }

    for device in data.values():
        brand=device.get("brand","").lower().strip()

        if brand in stats:
            stats[brand]["price"].append(device.get("price",0))
            stats[brand]["rating"].append(device.get("rating",0))

    def cal_mean(values: list[float]) -> float:
        if not values:
            return 0
        return round(sum(values) / len(values), 2)
    
    avg_price_1 = cal_mean(stats[brand1]["price"])
    avg_price_2 = cal_mean(stats[brand2]["price"])

    premium_brand = (
        brand1 if avg_price_1 > avg_price_2 else brand2
        if avg_price_2 > avg_price_1 else "equal"
    )

    return {
        "brand_1": {
            "name": brand1,
            "average_price": avg_price_1,
            "average_rating": cal_mean(stats[brand1]["rating"]),
            "product_count": len(stats[brand1]["price"])
        },
        "brand_2": {
            "name": brand2,
            "average_price": avg_price_2,
            "average_rating": cal_mean(stats[brand2]["rating"]),
            "product_count": len(stats[brand2]["price"])
        },
        "premium_heavy_brand": premium_brand
    }




    
    





