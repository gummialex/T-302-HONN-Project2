from fastapi import FastAPI
import uvicorn

from routers.order_endpoints import router as order_router

app = FastAPI()
app.include_router(order_router)


if __name__ == '__main__':
    uvicorn.run('startup:app', host='0.0.0.0', port=8000, reload=False)