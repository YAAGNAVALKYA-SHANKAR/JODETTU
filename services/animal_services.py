import base64, csv, io, shutil
from fastapi import HTTPException
from collections import OrderedDict
from general.database import own_animals, market_animals
from models.animal_model import OwnAnimalBase
from datetime import date
from services import taxes,discounts,convenience_fees,vaccinations
UPLOAD_DIR="upload_files"
class OwnAnimalServices:
    @staticmethod
    async def add_new_animal(animal_data,files):
        counter_doc=await own_animals.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        own_animal_id=f"OWN_{counter_value:02d}"
        ordered_data=OrderedDict([("own_animal_id",own_animal_id),*animal_data.dict().items()])
        ordered_data["own_animal_last_vacc"]=ordered_data["own_animal_last_vacc"].isoformat()
        file_data=[]
        for file in files:
            file_content=await file.read()
            base64_string=base64.b64encode(file_content).decode("utf-8")
            file_data.append({"filename":file.filename,"data":base64_string})
        ordered_data["images"]=file_data
        await own_animals.insert_one(ordered_data)
        await own_animals.update_one({"function":"ID_counter"},{"$inc": {"count":1}},upsert=True)
        return HTTPException(status_code=200,detail=f"Animal {ordered_data['own_animal_name']} added successfully.")
    @staticmethod
    async def list_all_animals():
        exclude_filter = {"function": "ID_counter"}
        doc_cursor = own_animals.find()
        docs = await doc_cursor.to_list(length=None)
        updated_docs = []
        for doc in docs:
            if all(doc.get(k) == v for k, v in exclude_filter.items()):
                continue
            updated_doc = vaccinations.VaccinationHelper.process_animal_vaccinations(doc)
            updated_doc["_id"] = str(doc["_id"])
            updated_docs.append(updated_doc)
        return updated_docs
    @staticmethod
    async def search_animal(animal_id):
        existing_animal=await own_animals.find_one({"own_animal_id":animal_id})
        if not existing_animal:raise HTTPException(status_code=404,detail=f"Animal {animal_id} not found!")
        else:return OwnAnimalBase(**existing_animal).model_dump()
    @staticmethod
    async def update_animal(data,animal_id):
        existing_animal=await own_animals.find_one({"own_animal_id":animal_id})
        if not existing_animal:raise HTTPException(status_code=404,detail=f"Animal {animal_id} not found")
        dict_data=data.model_dump()
        dict_data["own_animal_last_vacc"]=dict_data["own_animal_last_vacc"].isoformat()
        result=await own_animals.update_one({"own_animal_id":animal_id},{"$set":dict_data})
        if result.modified_count:raise HTTPException(status_code=200,detail=f"Animal {animal_id} updated successfully!")
        else:raise HTTPException(status_code=400,detail="No changes detected!")
    @staticmethod
    async def delete_animal(animal_id):
        existing_animal=await own_animals.find_one({"own_animal_id":animal_id})
        if not existing_animal:raise HTTPException(status_code=404,detail=f"Animal {animal_id} not found!")
        else:
            own_animals.delete_one({"own_animal_id":animal_id})
            raise HTTPException(status_code=200,detail=f"Animal {animal_id} deleted successfully!")
    @staticmethod
    async def import_animals_with_images(csv_file,image_files):
        try:    
            csv_bytes=await csv_file.read()
            csv_text=io.StringIO(csv_bytes.decode("utf-8"), newline="")
            csv_reader=csv.DictReader(csv_text)
            animals_data=list(csv_reader)
            image_lookup={file.filename:file for file in image_files}
            inserted=0
            for animal in animals_data:
                image_filenames=[name.strip() for name in animal.get("images", "").split(";")if name.strip()]
                matched_files=[]
                for name in image_filenames:
                    if name in image_lookup:
                        upload_file=image_lookup[name]
                        await upload_file.seek(0)
                        file_location=f"{UPLOAD_DIR}/{upload_file.filename}"
                        with open(file_location, "wb") as buffer: shutil.copyfileobj(upload_file.file,buffer)
                        await upload_file.seek(0)
                        matched_files.append(upload_file)
                    else: raise HTTPException(status_code=400,detail=f"Image {name} not found in upload.")
                try:
                    animal["own_animal_last_vacc"]=date(animal["own_animal_last_vacc"]).isoformat()
                    animal_model=OwnAnimalBase(
                        own_animal_type=animal["own_animal_type"],
                        own_animal_breed=animal["own_animal_breed"],
                        own_animal_name=animal["own_animal_name"],
                        own_animal_age=int(animal["own_animal_age"]),
                        own_animal_height=float(animal["own_animal_height"]),
                        own_animal_weight=float(animal["own_animal_weight"]),
                        own_animal_last_vacc=date(animal["own_animal_last_vacc"]),
                        own_animal_desc=animal["own_animal_desc"],)
                except Exception as e:raise HTTPException(status_code=422,detail=f"Invalid data format: {str(e)}")
                await OwnAnimalServices.add_new_animal(animal_model,matched_files)
                inserted+=1
            return {"message":f"Successfully imported {inserted} animals."}
        except Exception as e:raise HTTPException(status_code=500,detail=str(e))        
    @staticmethod
    async def sell_animals(animal_id,market_price,location):
        existing_animal=await own_animals.find_one({"own_animal_id":animal_id})
        if not existing_animal:raise HTTPException(status_code=404,detail=f"Animal {animal_id} not found")
        else:
            counter_doc=await market_animals.find_one({"function": "ID_counter"})
            counter_value=counter_doc["count"]if counter_doc else 1
            market_animal_id=f"Ph.No_{animal_id}_{counter_value:02d}"
            already_on_market=await market_animals.find_one({"market_animal_id":market_animal_id})
            if already_on_market: raise HTTPException(status_code=400,detail=f"Animal {animal_id} is already on the market")
            else:
                existing_animal.pop("own_animal_id",None)
                existing_animal.pop("_id",None)
                ordered_data=OrderedDict([
                    ("market_animal_id",market_animal_id),
                    ("market_price",market_price), 
                    *existing_animal.items(),
                    ("location",location)],)
                await market_animals.insert_one(ordered_data)
                await market_animals.update_one({"function":"ID_counter"},{"$inc":{"count": 1}},upsert=True)
                return HTTPException(status_code=200,detail=f"Animal {animal_id} added to the market successfully")
    @staticmethod
    async def list_all_market_animals():
        exclude_filter={"function":"ID_counter"}
        doc_cursor=market_animals.find()
        docs=await doc_cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    @staticmethod
    async def buy_animal(animal_id):
        existing_animal=await market_animals.find_one({"market_animal_id":animal_id})
        if not existing_animal:raise HTTPException(status_code=404,detail=f"Animal {animal_id} not found")
        else:
            price=await market_animals.find_one({"market_animal_id":animal_id},{"_id": 0,"market_price":1})
            base_price=price["market_price"]
            tax=await taxes.TaxCalculator.calculate_taxes(price)
            discount=await discounts.Discount.discount_calculator(price)
            convenience_fee=await convenience_fees.Convenience.convenience_fee_calculator(price)
            final_price=(base_price+tax+convenience_fee)-discount 
            price_data={"base_price":base_price,"tax":tax,"discount":discount,"final_price":final_price,"convenince_fee":convenience_fee}
            return(price_data)