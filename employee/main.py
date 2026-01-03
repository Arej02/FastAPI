from fastapi import FastAPI,HTTPException,Path
from fastapi.responses import JSONResponse
from pathlib import Path as path
from typing import List
from model import Employee
import json 

app=FastAPI()
base_url=path.cwd().parent
file_url=base_url/"data"/"employee.json"
print(base_url)

def load_data(url):
    with open(url,'r') as f:
        data=json.load(f)
    return data

def save_data(url,data):
    with open(url,'w') as f:
        json.dump(data,f,indent=4)
        print("Saved to the database")

@app.get("/")
def home():
    return {'message':'Welcome to the employee database'}

# 1) Read all employee:
@app.get("/allemployee")
def get_employees():

    data=load_data(file_url)

    return {
        "employees":data
    }

# 2) Read specific employee:
@app.get("/allemployee/{id}")
def get_employees(id:int=Path(...,description="Enter the id",example=2)):

    data=load_data(file_url)
    result={}
    for employees,details in data.items():
        for info in details:
            db_id=info.get("id",0)
            if db_id==id:
                return {
                    "success":True,
                    "details":info
                }
            
    if result is None:
        raise HTTPException(status_code=500,description="The id does not exist")
    

# 3) Add an employee:
@app.post("/create")
def create_employee(employee:Employee):
    data=load_data(file_url)
    employee_list=data.get("employees",[])

    for values in employee_list:
        db_id=values.get("id",0)

        if db_id==employee.id:
            raise HTTPException(status_code=400,detail="The employee already exists")
        
    employee_list.append(employee.model_dump())

    save_data(file_url,data)

    return JSONResponse(
        status_code=201, 
        content={"message": "Employee added successfully", "data": employee.model_dump()}
    )




    



    






