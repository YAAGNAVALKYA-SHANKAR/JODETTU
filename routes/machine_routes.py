from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.machine_services import MachineServices
from models.machine_model import MachineBase
service=MachineServices()
router=APIRouter()
@router.post("/add-machine")
async def add_new_machine(
    machine_name:str=Form(...),
    machine_brand:str=Form(...),
    machine_price:float=Form(...),
    machine_desc:str=Form(...),
    files:list[UploadFile]=File(...),):
    try:
        machine_data=MachineBase(
            machine_name=machine_name,
            machine_brand=machine_brand,
            machine_price=machine_price,
            machine_desc=machine_desc,)
        return await service.add_new_machine(machine_data,files)
    except Exception as e:raise HTTPException(status_code=400,detail=str(e))
@router.post("/buy/{machine_id}")
async def buy_machine(machine_id):return await service.buy_machine(machine_id)
@router.get("/all-machines")
async def get_all_machines():return await service.list_all_machines()
@router.put("/update-machine/{machine_name}")
async def update_machine(data:MachineBase,machine_name:str):return await service.update_machine(data,machine_name)
@router.delete("/delete-machine/{machine_name}")
async def delete_machine(machine_name):return await delete_machine(machine_name)
@router.post("bulk-upload")
async def bulk_upload(csv_file:UploadFile=File(...),files:list[UploadFile]=File(...)):return await service.bulk_import_machines(csv_file,files)