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


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)




@app.get("/")
async def root() -> APIResponse:

    return APIResponse(success=True, message="App Test Successful", payload=None)
