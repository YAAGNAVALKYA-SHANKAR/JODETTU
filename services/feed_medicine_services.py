from fastapi import HTTPException, APIRouter
from models.product_model import ProductBase
from general.database import feed_medicines
from services import taxes, discounts, convenience_fees
from collections import OrderedDict
router = APIRouter()
class FeedMedicineServices:
    @staticmethod
    async def add_new_feed(feed_data):        
        dict_data=feed_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        counter_doc=await feed_medicines.find_one({"function":"ID_counter"})
        counter_value=counter_doc["feed_count"] if counter_doc else 1
        feed_id=f"FEED_{counter_value:02d}"
        ordered_data=OrderedDict([("id",feed_id),*dict_data.items()])
        await feed_medicines.insert_one(ordered_data)
        await feed_medicines.update_one({"function":"ID_counter"},{"$inc":{"feed_count": 1}},upsert=True)
        return HTTPException(status_code=200,detail="Feed added successfully!")        
    @staticmethod   
    async def add_new_medicine(medicine_data):
        dict_data=medicine_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        counter_doc=await feed_medicines.find_one({"function":"ID_counter"})
        counter_value=counter_doc["med_count"]if counter_doc else 1
        medicine_id=f"MED_{counter_value:02d}"
        ordered_data=OrderedDict([("id",medicine_id),*dict_data.items()])
        await feed_medicines.insert_one(ordered_data)
        await feed_medicines.update_one({"function":"ID_counter"},{"$inc":{"med_count":1}},upsert=True)
        return HTTPException(status_code=200,detail="Medicine added successfully!")        
    @staticmethod 
    async def list_feed_medicines():
        exclude_filter={"function":"ID_counter"}
        doc_cursor=feed_medicines.find()
        docs=await doc_cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    @staticmethod
    async def search_product(id):
        existing_product=await feed_medicines.find_one({"id":id})
        if not existing_product:raise HTTPException(status_code=404,detail=f"Product {id} not found")
        else:return ProductBase(**existing_product).model_dump()
    @staticmethod
    async def update_feed(feed_id,feed_data):
        dict_data=feed_data.model_dump()
        dict_data["expiry_date"]=dict_data["expiry_date"].isoformat()
        existing_feed=await feed_medicines.find_one({"id":feed_id})
        if not existing_feed:raise HTTPException (status_code=404,detail=f"Feed {feed_id} not found")
        else:
            result=await feed_medicines.update_one({"id":feed_id},{"$set":dict_data})
            if result.modified_count:return HTTPException(status_code=200,detail=f"Feed {feed_id} updated successfully")
            else:raise HTTPException(status_code=400,detail="No changes detected")
    @staticmethod
    async def update_medicine(medicine_id, medicine_data):
        dict_data=medicine_data.model_dump()
        dict_data["expiry_data"]=dict_data["expiry_date"].isoformat()
        existing_medicine=await feed_medicines.find_one({"id":medicine_id})
        if not existing_medicine:raise HTTPException (status_code=404,detail=f"Medicine {medicine_id} not found")
        else:
            result=await feed_medicines.update_one({"id":medicine_id},{"$set":dict_data})
            if result.modified_count:return HTTPException (status_code=200,detail=f"Medicine {medicine_id} updated successfully")
            else:raise HTTPException (status_code=400,detail="No changes detected")
    @staticmethod
    async def delete_product(product_id):
        existing_feed=await feed_medicines.find_one({"id":product_id})
        if not existing_feed:raise HTTPException(status_code=404,detail=f"Product {product_id} not found")
        else:
            feed_medicines.delete_one({"id":product_id})
            return HTTPException(status_code=200,detail=f"Product {product_id} deleted successfully")
    @staticmethod
    async def buy_feed(feed_id):
        price=await feed_medicines.find_one({"id":feed_id},{"_id":0,"feed_price":1})
        base_price=price["price"]
        tax=await taxes.TaxCalculator.calculate_taxes(price)
        discount=await discounts.Discount.discount_calculator(price)
        convenience_fee=await convenience_fees.Convenience.convenience_fee_calculator(price)
        final_price=(base_price+tax+convenience_fee)-discount 
        price_data={"base_price":base_price,"tax":tax,"discount":discount,"final_price":final_price,"convenience_fee":convenience_fee}
        return (price_data)    
    @staticmethod
    async def buy_medicine(medicine_id):
        price=await feed_medicines.find_one({"id":medicine_id},{"_id": 0,"medicine_price":1})
        base_price=price["price"]
        tax=await taxes.TaxCalculator.calculate_taxes(price)
        discount=await discounts.Discount.discount_calculator(price)
        convenience_fee=await convenience_fees.Convenience.convenience_fee_calculator(price)
        final_price=(base_price+tax+convenience_fee)-discount 
        price_data={"base_price":base_price,"tax":tax,"discount":discount,"final_price":final_price,"convenience_fee":convenience_fee}
        return (price_data)