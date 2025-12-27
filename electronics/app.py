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
    
    # Compare the average price, average rating, number of products, which brand is premium-heavy:

    stats={
        "brand1":{
            "price":[],
            "rating":[]
        },
        "brand2":{
            "price":[],
            "rating":[]
        }
    }

    for device_id,device in data.items():
        brand_name=device.get("brand").strip().lower()
        if brand_name==brand1:
            stats["brand1"]["price"].append(device.get("price",0))
            stats["brand1"]["rating"].append(device.get("rating",0))

        if brand_name==brand2:
            stats["brand2"]["price"].append(device.get("price",0))
            stats["brand2"]["rating"].append(device.get("rating",0))

    def calcualte_avg(list_num):
        return round(sum(list_num)/len(list_num),2) if list_num else 0
    
    avg_price1=calcualte_avg(stats["brand1"]["price"])
    avg_price2=calcualte_avg(stats["brand2"]["price"])

    avg_rating1=calcualte_avg(stats["brand1"]["rating"])
    avg_rating2=calcualte_avg(stats["brand2"]["rating"])

    comparision_result=(
        brand1 if avg_price1>avg_price2 else brand2
        if avg_price2>avg_price1 else "Equal"
    )

    return {
        "brand1":f"{brand1} has avg. price:{avg_price1}, avg. rating:{avg_rating1}",
        "brand2":f"{brand2} has avg. price:{avg_price2}, avg. rating:{avg_rating2}",
        "premium_brand":f"{comparision_result}"

    }


@app.get("/product/power/{number}")
def get_power(number:int=Path(...,description="Enter the n devices you need based on power",example=2,ge=1)):

    data=load_data(file_path)

    result=[]
    for device_id,device in data.items():
        power=device.get("power_usage_watts")
        device_name=device.get("name")
        result.append({
            "device_id": device_id,
            "name": device_name,
            "power_usage_watts": power
        })
        
    top_n=sorted(result,key=lambda x:x["power_usage_watts"],reverse=True)[:number]

    return {
        "count":len(top_n),
        "devices":top_n
    }
    

@app.get("/most_commom_feature/{n}")
def get_power(n:int=Path(...,description="The n most common feature")):
    data=load_data(file_path)

    count_dict={}

    for value in data.values():
        features=value.get("features",[])
        for feature in features:
            count_dict[feature]=count_dict.get(feature,0)+1

    sort_dict=dict(sorted(count_dict.items(),key=lambda x:x[1],reverse=True)[:n])

    return {
        "data":sort_dict
    }



