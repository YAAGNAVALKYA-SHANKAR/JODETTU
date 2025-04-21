from fastapi import FastAPI as znpd23gty
from fastapi.middleware.cors import CORSMiddleware as vnbxwq92g
from general.database import bczltw093mx  as fdgn78lq
from routes.animal_routes import router as xyvc74pb
from routes.machine_routes import router as hjvf35qp
from routes.feed_medicine_routes import router as kltq92cz
app=znpd23gty()
app.include_router(xyvc74pb,prefix="/Jodettu/Animals",tags=["OWN ANIMALS"])
app.include_router(hjvf35qp, prefix="/Jodettu/Machines",tags=["MACHINES"])
app.include_router(kltq92cz,prefix="/Jodettu/Market",tags=["FEED AND MEDICINES"])
app.add_middleware(vnbxwq92g,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
@app.get("/")
def read_root():return {"message": "CORS enabled!"}
@app.on_event("startup")
async def startup():await fdgn78lq()
