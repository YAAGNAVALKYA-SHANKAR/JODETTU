import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
DATABASE=os.getenv("ANIMAL_DATABASE")
OWN_ANIMALS=os.getenv("OWN_ANIMALS")
MARKET_ANIMALS=os.getenv("MARKET_ANIMALS")
MACHINES=os.getenv("MACHINES")
FEED_MEDICINES=os.getenv("FEED_MEDICINES")

client=AsyncIOMotorClient(MONGO_URI)
db=client[DATABASE]
own_animals=db[OWN_ANIMALS]
market_animals=db[MARKET_ANIMALS]
machines=db[MACHINES]
feed_medicines=db[FEED_MEDICINES]

async def init_db():
    UPLOAD_DIR="upload_files"
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    existing_collections=await db.list_collection_names()
    async def create_collection_with_counter(collection_name):
        if collection_name not in existing_collections:
            await db.create_collection(collection_name)
            await db[collection_name].insert_one({"function":"ID_counter","count":1})
    await create_collection_with_counter(OWN_ANIMALS)
    await create_collection_with_counter(MARKET_ANIMALS)
    await create_collection_with_counter(MACHINES)
    if FEED_MEDICINES not in existing_collections:
        await db.create_collection(FEED_MEDICINES)
        await feed_medicines.insert_one({"function":"ID_counter","med_count":1,"feed_count":1})
    await own_animals.create_index([("own_animal_id",ASCENDING)],unique=True)
    await market_animals.create_index([("market_animal_id",ASCENDING)],unique=True)
    await machines.create_index([("machine_id",ASCENDING)],unique=True)
    await feed_medicines.create_index([("id",ASCENDING)],unique=True)