from pydantic import BaseModel,Field
from datetime import date
class MedicineBase(BaseModel):
    medicine_name:str=Field(...)
    medicine_brand:str=Field(...)
    medicine_composition:str=Field(...)
    medicine_animal:str=Field(...)
    meddicine_manufacturer:str=Field(...)
    medicine_price:float=Field(...)
    medicine_expiry_date:date=Field(...)