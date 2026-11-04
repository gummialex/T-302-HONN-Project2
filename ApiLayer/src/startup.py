from fastapi import FastAPI

from routers.order_endpoints import router as order_router
from routers.merchant_endpoints import router as merchant_router
from routers.buyer_endpoints import router as buyer_router
from routers.product_endpoints import router as product_router

app = FastAPI()

app.include_router(order_router)
app.include_router(merchant_router)
app.include_router(buyer_router)
app.include_router(product_router)