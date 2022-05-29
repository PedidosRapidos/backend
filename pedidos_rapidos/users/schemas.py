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

class UserResponse(BaseModel):
    id: int | None = None
    email: str
    username: str
    cartId : int | None

class LoginUserRequest(BaseModel):
    email: str
    password: str
    token: str | None = None

class LoginUserResponse(BaseModel):
    id: int | None = None
    email: str
    username: str
    isOwner: bool
    isClient: bool
    cartId : int | None
