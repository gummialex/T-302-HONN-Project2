from pydantic import BaseModel

class Merchant(BaseModel):
    name: str
    ss: str
    email : str
    phoneNumber :  str
    allowsDiscount : bool

