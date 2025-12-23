from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,List
from datetime import datetime

class DevicesSchema(BaseModel):
    price:Annotated[int,Field(
        ...,title="Price",
        description="Enter the price of the phone",
        example=1500,gt=0
        )]
    stock:Annotated[int,Field(
        ...,title="Stock",
        description="Enter the stock of the phone",
        example=40,ge=0
        )]
    rating:Annotated[float,Field
                     (...,title="Rating",
                    description="Enter the rating of the phone",
                    example=3.5,ge=0,le=5
                    )]
    launch_year:Annotated[int,Field(
        ...,title="Launc Year",
        description="Enter the year of launc",
        ge=2000
    )]
    category:Literal["smartphone","laptop","headphones","tablet"]
    features:List[str]

    @computed_field
    @property
    def price_category(self)->str:
        if self.price<=500:
            return "budget"
        elif self.price<=1200:
            return "midrange"
        return "premium"
        
    @computed_field
    @property
    def availability(self)->str:
        if self.stock==0:
            return "out_of_stock"
        else:
            return "in_stock"
        
    @computed_field
    @property
    def device_age(self)->int:
        current_year = datetime.now().year
        return max(0,current_year-self.launch_year) # Do not want the device age to be negative