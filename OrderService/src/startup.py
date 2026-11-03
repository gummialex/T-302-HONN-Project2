from fastapi import FastAPI

from routers.order_endpoints import router as order_router

app = FastAPI()
app.include_router(order_router)

