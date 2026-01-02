from sqlalchemy.orm import Session
from model import Employee
import schemas


def get_employees(db:Session):
    return db.query(Employee).all()

def get_employee(db:Session, id:int):
    return (
        db
        .query(Employee)
        .filter(Employee.id==id)
        .first()
        )

def create_employee(db:Session,employee:schemas.CreateEmployee):
    new_employee=Employee(
        name=employee.name,
        email=employee.email
    )
    db.add(new_employee)
    db.commit() 
    db.refresh(new_employee) 

    return new_employee

def update_employee(db:Session,emp_id:int, employee:schemas.UpdateEmployeeEmployee):
    db_employee=db.query(Employee).filter(Employee.id==emp_id).first()
    if db_employee:
        db_employee.name=employee.name
        db_employee.email=employee.email
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db:Session,emp_id:int):
    db_employee=db.query(Employee).filter(emp_id==Employee.id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()

    return db_employee


