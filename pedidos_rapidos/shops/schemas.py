import email
from pydantic import BaseModel


class ShowShopRequest(BaseModel):
    name: str
    address: str
    cbu: str

class ShowShopResponse(BaseModel):
    id: int | None = None
    name: str
    address: str
    cbu: str
