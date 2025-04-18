from pydantic import BaseModel,Field
from datetime import date
class ProductBase(BaseModel):
    name:str=Field(...)
    brand:str=Field(...)
    composition:str=Field(...)
    animal:str=Field(...)
    manufacturer:str=Field(...)
    price:float=Field(...)
    expiry_date:date=Field(...)
    