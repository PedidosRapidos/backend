import email
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    confirmPassword: str
    isOwner: bool
    isClient: bool

class CreateUserResponse(BaseModel):
    id: int | None = None
    email: str
    username: str

class LoginUserRequest(BaseModel):
    email: str
    password: str

class LoginUserResponse(BaseModel):
    id: int | None = None
    email: str
    username: str
    isOwner: bool
    isClient: bool
