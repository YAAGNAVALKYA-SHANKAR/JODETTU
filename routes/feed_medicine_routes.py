from fastapi import FastAPI, HTTPException, APIRouter, Form
from services.feed_medicine_services import FeedMedicineServices
from models.feed_model import FeedBase
from models.medicines_model import MedicineBase
from datetime import date
service=FeedMedicineServices()
router = APIRouter()
@router.post("/add-feed")
async def add_feed(
    feed_name: str = Form(...),
    feed_type: str = Form(...),
    feed_animal: str = Form(...),
    feed_price: str = Form(...),
    feed_expiry_date: date = Form(...),
):
    try:
        feed_data = FeedBase(
            feed_name=feed_name,
            feed_type=feed_type,
            feed_animal=feed_animal,
            feed_price=feed_price,
            feed_expiry_date=feed_expiry_date
        )
        return await service.add_new_feed(feed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"This is the flag raised{e}")

        
@router.post("/add-medicine")
async def add_new_medicine(
        medicine_name:str=Form(...),
        medicine_brand:str=Form(...),
        medicine_composition:str=Form(...),
        meddicine_manufacturer:str=Form(...),
        medicine_price:float=Form(...),
        medicine_expiry_date:date=Form(...),    
    ):
     
        try:
            medicine_data = MedicineBase(
                medicine_name=medicine_name,
                medicine_brand=medicine_brand,
                medicine_composition=medicine_composition,
                meddicine_manufacturer=meddicine_manufacturer,
                medicine_price=medicine_price,
                medicine_expiry_date=medicine_expiry_date
            )
            return await service.add_new_medicine(medicine_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
@router.get("/all-feed")
async def list_all_feed():
     return await service.list_feed()

@router.get("/all-medicines")
async def list_all_medicines():
     return await service.list_medicines()