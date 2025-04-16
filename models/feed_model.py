from pydantic import BaseModel,Field
from datetime import date
class FeedBase(BaseModel):
    feed_name:str=Field(...)
    feed_brand:str=Field(...)
    feed_composition:str=Field(...)
    feed_manufacturer:str=Field(...)
    feed_price:float=Field(...)
    feed_expiry_date:date=Field(...)
    