from fastapi import HTTPException,APIRouter,Form,UploadFile,File
from services.feed_medicine_services import MarketServices
from models.product_model import ProductModel
from datetime import datetime
service=MarketServices()
router=APIRouter()
@router.post("/add-feed")
async def add_feed(
    feed_name:str=Form(...),
    feed_brand:str=Form(...),
    feed_composition:str=Form(...),
    feed_animal:str=Form(...),
    feed_manufacturer:str=Form(...),
    feed_price:float=Form(...),
    feed_expiry_date:datetime=Form(...),
    files:list[UploadFile]=File(...),):
    try:
        product_data=ProductModel(
            name=feed_name,
            brand=feed_brand,
            composition=feed_composition,
            animal=feed_animal,
            manufacturer=feed_manufacturer,
            price=feed_price,
            expiry_date=feed_expiry_date)
        return await service.add_feed(product_data, files)
    except Exception as e:raise HTTPException(status_code=400,detail=f"This is the flag raised{e}")        
@router.post("/add-medicine")
async def add_new_medicine(
        medicine_name:str=Form(...),
        medicine_brand:str=Form(...),
        medicine_composition:str=Form(...),
        medicine_animal:str=Form(...),
        medicine_manufacturer:str=Form(...),
        medicine_price:float=Form(...),
        medicine_expiry_date:datetime=Form(...),
        files:list[UploadFile]=File(...),):     
        try:
            product_data=ProductModel(
                name=medicine_name,
                brand=medicine_brand,                
                composition=medicine_composition,
                animal=medicine_animal,
                manufacturer=medicine_manufacturer,
                price=medicine_price,
                expiry_date=medicine_expiry_date)
            return await service.add_medicine(product_data,files)
        except Exception as e:raise HTTPException(status_code=400,detail=str(e))        
@router.get("/all-products")
async def list_all_products():return await service.list_all_products()
@router.put("/update-feed/{feed_id}")
async def update_feed(feed_data:ProductModel,feed_id:str):return await service.update_feed(feed_id,feed_data)
@router.put("/update-medicine/{medicine_id}")
async def update_medicine(medicine_data:ProductModel,medicine_id:str):return await service.update_medicine(medicine_id,medicine_data)
@router.delete("/delete-feed/{feed_id}")
async def delete_product(product_id:str):return await service.delete_product(product_id)
@router.post("/buy-feed/{feed_id}")
async def buy_feed(feed_id:str):return await service.buy_feed(feed_id)
@router.post("/buy-medicine/{medicine_id}")
async def buy_medicine(medicine_id:str):return await service.buy_medicine(medicine_id)
@router.get("/search/{product_id}")
async def search_product(product_id:str):return await service.search_product(product_id)
@router.post("/import-products")
async def import_products(csv_file:UploadFile=File(...),product_images:list[UploadFile]=File(...)):return await service.bulk_import_products(csv_file,product_images)