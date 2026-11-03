from fastapi import FastAPI
import uvicorn

from routers.order_endpoints import router as order_router

app = FastAPI()
app.include_router(order_router)

