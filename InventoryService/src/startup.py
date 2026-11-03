from fastapi import FastAPI
from src.routers.inventory_endpoints import router


app = FastAPI()

app.include_router(router)