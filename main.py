from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from general.database import init_db
from routes.own_animal_routes import router as own_animal_router
from routes.machine_routes import router as machine_router
from routes.feed_medicine_routes import router as feed_medicine_router
app=FastAPI()
app.include_router(own_animal_router,prefix="/Jodettu",tags=["OWN ANIMALS"])
app.include_router(machine_router, prefix="/Jodettu",tags=["MACHINES"])
app.include_router(feed_medicine_router,prefix="/Jodettu",tags=["FEED AND MEDICINES"])
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
@app.get("/")
def read_root():return {"message": "CORS enabled!"}
@app.on_event("startup")
async def startup():await init_db()