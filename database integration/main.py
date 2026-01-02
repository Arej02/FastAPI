from sqlalchemy.orm import Session
from database import engine,session,Base
from fastapi import FastAPI,HTTPException,Depends
import schemas
import curd

Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

# 1) Create Endpoint:
@app.get("/")
def home():
    return {"message":"Welcome to the home page"}

@app.post("/employees")
def create(employee:schemas.CreateEmployee,db:Session=Depends(get_db)):
    return curd.create_employee(db,employee)

# 2) Update Endpoint:
@app.post("/update/{employee_id}")
def create(employee_id:int,employee:schemas.UpdateEmployee,db:Session=Depends(get_db)):
    return curd.update_employee(db,employee_id,employee)

# 3) Get all employees:
@app.get("/allemployee")
def get_employees_db(db:Session=Depends(get_db)):
    return curd.get_employees(db)

# 4) Get specific employees:
@app.get("/allemployee/{emp_id}")
def get_employee_db(emp_id,db:Session=Depends(get_db)):
    employee=curd.get_employee(emp_id,db)

    if employee is None:
        raise HTTPException(status_code=404,detail="Employee not found")
    return employee


