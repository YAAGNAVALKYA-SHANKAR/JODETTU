from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.own_animal_services import OwnAnimalServices
from models.own_animal_model import OwnAnimalBase
from datetime import date

service = OwnAnimalServices()
router = APIRouter()
@router.post("/add-animal")
async def add_new_animal(
    own_animal_type: str = Form(...),
    own_animal_breed: str = Form(...),
    own_animal_name: str = Form(...),
    own_animal_age: int = Form(...),
    own_animal_height: float = Form(...),
    own_animal_weight: float = Form(...),
    own_animal_last_vacc: date = Form(...),
    own_animal_desc: str = Form(...),
    files: list[UploadFile] = File(...)
):
    try:
        animal_data = OwnAnimalBase(
            own_animal_type=own_animal_type,
            own_animal_breed=own_animal_breed,
            own_animal_name=own_animal_name,
            own_animal_age=own_animal_age,
            own_animal_height=own_animal_height,
            own_animal_weight=own_animal_weight,
            own_animal_last_vacc=own_animal_last_vacc,
            own_animal_desc=own_animal_desc
        )
        return await service.add_new_animal(animal_data, files)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/all_animals")
async def list_all_animals():
    return await service.list_all_animals()

@router.put("/update/{own_animal_id}")
async def update_animal(data:OwnAnimalBase, own_animal_id:str):
    return await service.update_animal(data, own_animal_id)

@router.delete("/{animal_id}")
async def delete_animal(animal_id:str):
    return await service.delete_animal(animal_id)

@router.get("/{animal_id}")
async def search_animal(animal_id):
    return await service.search_animal(animal_id)

@router.post("/import-csv-images/")
async def import_animals_from_csv(
    csv_file: UploadFile = File(...),
    image_files: list[UploadFile] = File(...)
):
    return await service.import_animals_with_images(csv_file, image_files)
