import base64,csv,shutil,io
from fastapi import HTTPException
from collections import OrderedDict
from datetime import datetime
from models.product_model import ProductModel
from general.database import market
from services import taxes,discounts,convenience_fees
UPLOAD_FILES="upload_files"
class MarketServices:
    @staticmethod
    async def add_feed(product_data,images):        
        dict_data=product_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        counter_doc=await market.find_one({"function":"ID_counter"})
        counter_value=counter_doc["feed_count"]if counter_doc else 1
        product_id=f"FEED_{counter_value:02d}"
        ordered_data=OrderedDict([("id",product_id),*dict_data.items()])
        file_data=[]
        for image in images:
            file_content=await image.read()
            base64_string=base64.b64encode(file_content).decode("utf-8")
            file_data.append({"filename":image.filename,"data":base64_string})
        ordered_data["images"]=file_data
        await market.insert_one(ordered_data)
        await market.update_one({"function":"ID_counter"},{"$inc":{"feed_count":1}},upsert=True)
        return HTTPException(status_code=200,detail="Feed added successfully!")        
    @staticmethod   
    async def add_medicine(product_data,images):
        dict_data=product_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        counter_doc=await market.find_one({"function":"ID_counter"})
        counter_value=counter_doc["med_count"]if counter_doc else 1
        product_id=f"MED_{counter_value:02d}"
        ordered_data=OrderedDict([("id",product_id),*dict_data.items()])
        file_data=[]
        for image in images:
            file_content=await image.read()
            base64_string=base64.b64encode(file_content).decode("utf-8")
            file_data.append({"filename":image.filename,"data":base64_string})
        ordered_data["images"]=file_data
        await market.insert_one(ordered_data)
        await market.update_one({"function":"ID_counter"},{"$inc":{"med_count":1}},upsert=True)
        return HTTPException(status_code=200,detail="Medicine added successfully!")        
    @staticmethod 
    async def list_all_products():
        exclude_filter={"function":"ID_counter"}
        cursor=market.find()
        docs=await cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    @staticmethod
    async def search_product(product_id):
        existing_product=await market.find_one({"id":product_id})
        if not existing_product:raise HTTPException(status_code=404,detail=f"Product {product_id} not found")
        else:existing_product["_id"]=str(existing_product["_id"])
        return existing_product
    @staticmethod
    async def update_feed(product_id,product_data):
        dict_data=product_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        existing_product=await market.find_one({"id":product_id})
        if not existing_product:raise HTTPException (status_code=404,detail=f"Feed {product_id} not found")
        else:
            result=await market.update_one({"id":product_id},{"$set":dict_data})
            if result.modified_count:return HTTPException(status_code=200,detail=f"Feed {product_id} updated successfully")
            else:raise HTTPException(status_code=400,detail="No changes detected")
    @staticmethod
    async def update_medicine(product_id,product_data):
        dict_data=product_data.model_dump()
        dict_data["expiry_data"]=dict_data["expiry_date"].isoformat()
        existing_product=await market.find_one({"id":product_id})
        if not existing_product:raise HTTPException (status_code=404,detail=f"Medicine {product_id} not found")
        else:
            result=await market.update_one({"id":product_id},{"$set":dict_data})
            if result.modified_count:return HTTPException (status_code=200,detail=f"Medicine {product_id} updated successfully")
            else:raise HTTPException (status_code=400,detail="No changes detected")
    @staticmethod
    async def delete_product(product_id):
        existing_product=await market.find_one({"id":product_id})
        if not existing_product:raise HTTPException(status_code=404,detail=f"Product {product_id} not found")
        else:market.delete_one({"id":product_id})
        return HTTPException(status_code=200,detail=f"Product {product_id} deleted successfully")
    @staticmethod
    async def buy_feed(product_id):
        price=await market.find_one({"id":product_id},{"_id":0,"price":1})
        base_price=price["price"]
        tax=await taxes.TaxCalculator.taxes(base_price)
        discount=await discounts.DiscountCalculator.discounts(base_price)
        conv_fees=await convenience_fees.ConvFeeCalculator.conv_fees(base_price)
        fial_price=(base_price+tax+conv_fees)-discount 
        price_data={"base_price":base_price,"tax":tax,"discount":discount,"final_price":fial_price,"convenience_fee":conv_fees}
        return(price_data)    
    @staticmethod
    async def buy_medicine(product_id):
        price=await market.find_one({"id":product_id},{"_id":0,"price":1})
        base_price=price["price"]
        tax=await taxes.TaxCalculator.taxes(base_price)
        discount=await discounts.DiscountCalculator.discounts(base_price)
        conv_fees=await convenience_fees.ConvFeeCalculator.conv_fees(base_price)
        final_price=(base_price+tax+conv_fees)-discount 
        price_data={"base_price":base_price,"tax":tax,"discount":discount,"final_price":final_price,"convenience_fee":conv_fees}
        return(price_data)
    @staticmethod
    async def bulk_import_products(csv_file,image_files,product_type):
        try:    
            csv_bytes=await csv_file.read()
            csv_text=io.StringIO(csv_bytes.decode("utf-8"),newline="")
            csv_reader=csv.DictReader(csv_text)
            product_data=list(csv_reader)
            image_lookup={w65thdrf65j.filename:w65thdrf65j for w65thdrf65j in image_files}
            inserted=0
            for product in product_data:
                image_filenames=[name.strip()for name in product.get("images","").split(";")if name.strip()]
                matched_files=[]
                for name in image_filenames:
                    if name in image_lookup:
                        upload_file=image_lookup[name]
                        await upload_file.seek(0)
                        file_location=f"{UPLOAD_FILES}/{upload_file.filename}"
                        with open(file_location, "wb") as buffer:shutil.copyfileobj(upload_file.file,buffer)
                        await upload_file.seek(0)
                        matched_files.append(upload_file)
                    else:raise HTTPException(status_code=400,detail=f"Image {name} not found in upload.")                
                    try:
                        product["expiry_date"]=datetime(product["expiry_date"]).isoformat()
                        product_model=ProductModel(
                                name=product["name"],
                                brand=product["brand"],
                                composition=product["composition"],
                                animal=product["animal"],
                                manufacturer=product["manufacturer"],
                                price=product["price"],
                                expiry_date=product["expiry_date"])
                    except Exception as e:raise HTTPException(status_code=422,detail=f"Invalid data format: {str(e)}")
                    if product_type=="feed":await MarketServices.add_feed(product_model,matched_files)
                    elif product_type=="medicines":await MarketServices.add_medicine(product_data,matched_files)
                    else:return HTTPException(status_code=400,detail="Invalid type")
                    inserted+=1
            return {"message":f"Successfully imported {inserted} animals."}
        except Exception as e:raise HTTPException(status_code=500,detail=str(e))