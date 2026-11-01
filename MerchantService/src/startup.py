from fastapi import FastAPI
from MerchantService.src.dtos.create_merchant_dto import Merchant

app = FastAPI()

@app.post("/merchant")
def create_mercant(merchant : Merchant):
    pass