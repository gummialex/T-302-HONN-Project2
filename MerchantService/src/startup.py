from fastapi import FastAPI
from src.routers.merchant_endpoints import router

app = FastAPI()

app.include_router(router)