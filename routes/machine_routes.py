from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from services.machine_services import MachineServices
from models.machine_model import MachineModel
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
        machine_data=MachineModel(
            machine_name=machine_name,
            machine_brand=machine_brand,
            machine_price=machine_price,
            machine_desc=machine_desc,)
        return await service.add_new_machine(machine_data,files)
    except Exception as e:raise HTTPException(status_code=400,detail=str(e))
@router.post("/buy/{machine_id}")
async def buy_machine(machine_id):return await service.buy_machine(machine_id)
@router.get("/all-machines")
async def get_all_machines():return await service.get_all_machines()
@router.put("/update-machine/{machine_name}")
async def update_machine(data:MachineModel,machine_id:str):return await service.update_machine(data,machine_id)
@router.delete("/delete-machine/{machine_name}")
async def delete_machine(machine_id):return await service.delete_machine(machine_id)
@router.post("bulk-upload")
async def bulk_upload(csv_file:UploadFile=File(...),files:list[UploadFile]=File(...)):return await service.bulk_upload_machines(csv_file,files)
@router.get("/search/{machine_id}")
async def search_machine(machine_id:str):return await service.search_machine_by_id(machine_id)