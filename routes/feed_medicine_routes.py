from fastapi import HTTPException, APIRouter, Form
from services.feed_medicine_services import FeedMedicineServices
from models.product_model import ProductBase
from datetime import date
service=FeedMedicineServices()
router = APIRouter()
@router.post("/add-feed")
async def add_feed(
    feed_name:str=Form(...),
    feed_brand:str=Form(...),
    feed_composition:str=Form(...),
    feed_animal:str=Form(...),
    feed_manufacturer:str=Form(...),
    feed_price:float=Form(...),
    feed_expiry_date:date=Form(...),):
    try:
        feed_data=ProductBase(
            name=feed_name,
            brand=feed_brand,
            composition=feed_composition,
            animal=feed_animal,
            manufacturer=feed_manufacturer,
            price=feed_price,
            expiry_date=feed_expiry_date)
        return await service.add_new_feed(feed_data)
    except Exception as e:raise HTTPException(status_code=400,detail=f"This is the flag raised{e}")        
@router.post("/add-medicine")
async def add_new_medicine(
        medicine_name:str=Form(...),
        medicine_brand:str=Form(...),
        medicine_composition:str=Form(...),
        medicine_animal:str=Form(...),
        medicine_manufacturer:str=Form(...),
        medicine_price:float=Form(...),
        medicine_expiry_date:date=Form(...),):     
        try:
            medicine_data=ProductBase(
                name=medicine_name,
                brand=medicine_brand,                
                composition=medicine_composition,
                animal=medicine_animal,
                manufacturer=medicine_manufacturer,
                price=medicine_price,
                expiry_date=medicine_expiry_date)
            return await service.add_new_medicine(medicine_data)
        except Exception as e:raise HTTPException(status_code=400,detail=str(e))        
@router.get("/all-products")
async def list_all_products():return await service.list_feed_medicines()
@router.put("/update-feed/{feed_id}")
async def update_feed(feed_data:ProductBase,feed_id:str):return await service.update_feed(feed_id,feed_data)
@router.put("/update-medicine/{medicine_id}")
async def update_medicine(medicine_data:ProductBase,medicine_id:str):return await service.update_medicine(medicine_id,medicine_data)
@router.delete("/delete-feed/{feed_id}")
async def delete_product(product_id:str):return await service.delete_product(product_id)
@router.post("/buy-feed/{feed_id}")
async def buy_feed(feed_id:str):return await service.buy_feed(feed_id)
@router.post("/buy-medicine/{medicine_id}")
async def buy_medicine(medicine_id:str):return await service.buy_medicine(medicine_id)