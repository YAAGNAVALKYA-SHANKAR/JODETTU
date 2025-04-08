from pydantic import BaseModel, Field
class MachineBase(BaseModel):
    machine_name:str=Field(...)
    machine_brand:str=Field(...)
    machine_price:float=Field(...)
    machine_desc:str=Field(...)