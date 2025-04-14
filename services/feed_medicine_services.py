from fastapi import HTTPException, APIRouter, Form
from models.feed_model import FeedBase
from models.medicines_model import MedicineBase
from datetime import date
from general.database import feed, medicines
from collections import OrderedDict
router = APIRouter()
class FeedMedicineServices:
    @staticmethod
    async def add_new_feed(feed_data):        
        dict_data = feed_data.model_dump()
        dict_data["feed_expiry_date"] = dict_data["feed_expiry_date"].isoformat()
        counter_doc=await feed.find_one({"function": "ID_counter"})
        counter_value=counter_doc["count"] if counter_doc else 1
        feed_id=f"FEED_{counter_value:02d}"
        ordered_data = OrderedDict([("feed_id", feed_id), *dict_data.items()])
        await feed.insert_one(ordered_data)
        await feed.update_one({"function": "ID_counter"}, {"$inc": {"count": 1}}, upsert=True)
        return HTTPException(status_code=200,detail="Feed added successfully!")
        
    @staticmethod   
    async def add_new_medicine(medicine_data):
        dict_data = medicine_data.model_dump()
        dict_data["medicine_expiry_date"] = dict_data["medicine_expiry_date"].isoformat()
        counter_doc=await medicines.find_one({"function": "ID_counter"})
        counter_value=counter_doc["count"] if counter_doc else 1
        medicine_id=f"MED_{counter_value:02d}"
        ordered_data = OrderedDict([("medicine_id", medicine_id), *dict_data.items()])
        await medicines.insert_one(ordered_data)
        await medicines.update_one({"function": "ID_counter"}, {"$inc": {"count": 1}}, upsert=True)
        return HTTPException(status_code=200, detail="Medicine added successfully!")
        
    @staticmethod 
    async def list_feed():
        exclude_filter={"function":"ID_counter"}
        doc_cursor= feed.find()
        docs=await doc_cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    
    @staticmethod
    async def list_medicines():
        exclude_filter={"function":"ID_counter"}
        doc_cursor= medicines.find()
        docs=await doc_cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    
    @staticmethod
    async def search_feed(feed_id):
        existing_feed=await feed.find_one({"feed_id":feed_id})
        if not existing_feed: raise HTTPException (status_code=404, detail=f"Feed {feed_id} not found")
        else: return FeedBase(**existing_feed).model_dump()

    @staticmethod
    async def search_medicine(medicine_id):
        existing_medicine=await medicines.find_one({"medicine_id":medicine_id})
        if not existing_medicine: raise HTTPException (status_code=404, detail=f"Medicine {medicine_id} not found")
        else: return MedicineBase(**existing_medicine).model_dump()