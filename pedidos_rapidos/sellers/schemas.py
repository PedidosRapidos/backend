from pydantic import BaseModel


class CreateShopRequest(BaseModel):
    address: str
    cbu: str

class CreateShopResponse(BaseModel):
    id: int | None = None
    address: str
    cbu: str
