from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.schemas.globals.responses import APIResponse    

#import models and default inventory
import app.api.models as models
from app.api.connection import engine, session
from .api.utils.utils import initialize_default_inventory


try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(e)


initialize_default_inventory(session)


###### import routers ######
from app.api.routers.products import products_router
from app.api.routers.admin import admin_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


##### register routers ######
app.include_router(products_router)
app.include_router(admin_router)


@app.get("/")
async def root() -> APIResponse:

    return APIResponse(success=True, message="App Test Successful", payload=None)
