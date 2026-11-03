from fastapi import FastAPI, APIRouter
from src.routers.buyer_endpoints import router

    
app = FastAPI()

app.include_router(router)