import os 
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
ANIMALS=os.getenv("ANIMALS")
OWN_ANIMALS=os.getenv("OWN_ANIMALS")
MARKET_ANIMALS=os.getenv("MARKET_ANIMALS")
MACHINES=os.getenv("MACHINES")
MARKET=os.getenv("MARKET")
client=AsyncIOMotorClient(MONGO_URI)
db=client[ANIMALS]
own_animals=db[OWN_ANIMALS]
market_animals=db[MARKET_ANIMALS]
machines=db[MACHINES]
market=db[MARKET]
async def init_db():
    UPLOAD_FILES="upload_files"
    os.makedirs(UPLOAD_FILES,exist_ok=True)
    existing_collections=await db.list_collection_names()
    async def create_collection_with_counter(collection):
        if collection not in existing_collections:
            await db.create_collection(collection)
            await db[collection].insert_one({"function":"ID_counter","count":1})
    await create_collection_with_counter(OWN_ANIMALS)
    await create_collection_with_counter(MARKET_ANIMALS)
    await create_collection_with_counter(MACHINES)
    if MARKET_ANIMALS not in existing_collections:
        await db.create_collection(MARKET_ANIMALS)
        await market.insert_one({"function":"ID_counter","med_count":1,"feed_count":1})
    await own_animals.create_index([("own_animal_id",ASCENDING)],unique=True)
    await market_animals.create_index([("market_animal_id",ASCENDING)],unique=True)
    await machines.create_index([("machine_id",ASCENDING)],unique=True)
    await market.create_index([("id",ASCENDING)],unique=True)