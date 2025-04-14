from pydantic import BaseModel, Field
from datetime import date
class FeedBase(BaseModel):
    feed_name:str=Field(...)
    feed_type:str=Field(...)
    feed_animal:str=Field(...)
    feed_price:str=Field(...)
    feed_expiry_date:date=Field(...)
    