import base64, shutil, os, pandas, csv, io, json
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from collections import OrderedDict
from general.database import machines
from models.machine_model import MachineBase
from services import discounts, taxes
UPLOAD_DIR="upload_files"
class MachineServices:
    @staticmethod
    async def add_new_machine(machine_data,files):
        counter_doc=await machines.find_one({"function": "ID_counter"})
        counter_value=counter_doc["count"] if counter_doc else 1
        data=machine_data.model_dump()
        prefix = data["machine_brand"][:3].upper()
        machine_id=f"{prefix}_{counter_value:02d}"
        ordered_data = OrderedDict([("machine_id", machine_id), *data.items()])
        file_data=[]
        for file in files:
            file_content = await file.read()
            base64_string = base64.b64encode(file_content).decode("utf-8")
            file_data.append({"filename": file.filename, "data": base64_string})
        ordered_data["images"] = file_data
        await machines.insert_one(ordered_data)
        await machines.update_one({"function": "ID_counter"}, {"$inc": {"count": 1}}, upsert=True)
        return HTTPException(status_code=200,detail=f"Machine {ordered_data['machine_name']} added successfully.")
    
    @staticmethod
    async def list_all_machines():
        exclude_filter={"function":"ID_counter"}
        doc_cursor= machines.find()
        docs=await doc_cursor.to_list(length=None)
        return[{**doc,"_id":str(doc["_id"])}for doc in docs if not all(doc.get(k)==v for k,v in exclude_filter.items())]
    
    @staticmethod
    async def update_machine(data, machine_name):
        existing_machine=await machines.find_one({"machine_name":machine_name})
        if not existing_machine:raise HTTPException(status_code=404, detail=f"Machine {machine_name} not found")
        dict_data=data.model_dump()
        result=await machines.update_one({"machine_name":machine_name},{"$set":dict_data})
        if result.modified_count:raise HTTPException(status_code=200,detail=f"Machine {machine_name} updated successfully!")
        else:raise HTTPException(status_code=400,detail="No changes detected!")
    @staticmethod
    async def delete_machine(machine_name):
        existing_machine=await machines.find_one({"machine_name":machine_name})
        if not existing_machine:raise HTTPException(status_code=404,detail=f"Machine {machine_name} not found!")
        else:
            machines.delete_one({"machine_name":machine_name})
            raise HTTPException(status_code=200,detail=f"Machine {machine_name} deleted successfully!")
        
    @staticmethod
    async def bulk_import_machines(csv_file, image_files):
        try:
            csv_bytes = await csv_file.read()
            csv_text = io.StringIO(csv_bytes.decode("utf-8"), newline="")
            csv_reader = csv.DictReader(csv_text)
            machines_data = list(csv_reader)

            image_lookup = {file.filename: file for file in image_files}

            inserted = 0

            for machine in machines_data:
                image_filenames = [name.strip() for name in machine.get("images", "").split(";") if name.strip()]
                matched_files = []

                for name in image_filenames:
                    if name in image_lookup:
                        upload_file = image_lookup[name]

                        await upload_file.seek(0)

                        file_location = f"{UPLOAD_DIR}/{upload_file.filename}"
                        with open(file_location, "wb") as buffer:
                            shutil.copyfileobj(upload_file.file, buffer)

                        await upload_file.seek(0)
                        matched_files.append(upload_file)
                    else:
                        raise HTTPException(status_code=400, detail=f"Image {name} not found in upload.")

                try:
                    machine_model = MachineBase(
                        machine_name=machine["machine_name"],
                        machine_brand=machine["machine_brand"],
                        machine_price=float(machine["machine_price"]),
                        machine_desc=machine["machine_desc"],
                    )
                except Exception as e:
                    raise HTTPException(status_code=422, detail=f"Invalid data format: {str(e)}")

                await MachineServices.add_new_machine(machine_model, matched_files)
                inserted += 1

            return {"message": f"Successfully imported {inserted} machines."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def buy_machine(machine_id):
        price = await machines.find_one({"machine_id": machine_id}, {"_id": 0, "machine_price": 1})
        base_price = price["machine_price"]
        tax = await taxes.TaxCalculator.calculate_taxes(price)
        discount = await discounts.Discount.discount_calculator(price)
        final_price = (base_price+tax)-discount 
        price_data = {"base_price": base_price,"tax": tax,"discount": discount,"final_price": final_price}
        return (price_data)