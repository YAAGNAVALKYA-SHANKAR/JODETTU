from pydantic import BaseModel, Field
from datetime import date
class OwnAnimalBase(BaseModel):
    own_animal_type:str=Field(...)
    own_animal_breed:str=Field(...)
    own_animal_name:str=Field(...)
    own_animal_age:int=Field(...)
    own_animal_height:float=Field(...)
    own_animal_weight:float=Field(...)
    own_animal_last_vacc:date=Field(...)
    own_animal_desc:str=Field(...)
class LocationBase(BaseModel):
    latitude:float=Field(...)
    longitude:float=Field(...)