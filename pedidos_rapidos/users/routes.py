import logging
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .exception import PasswordDontMatchException
from .exception import UserAlreadyCreatedException
from .. import database


router = APIRouter(prefix="/users")

logger = logging.getLogger("uvicorn")

@router.post("/register", response_model=schemas.CreateUserResponse)
def post_seller(
        create_user_req: schemas.CreateUserRequest,
        db: Session = Depends(database.get_db)):

    if create_user_req.password != create_user_req.confirmPassword:
        raise HTTPException(status_code=400, detail='Passwords dont match')

    try:
        if create_user_req.isOwner:
            user = crud.create_seller(db,
                                        database.Seller(**create_user_req.dict()))
        else:
            user = crud.create_client(db,
                                        database.Client(**create_user_req.dict()))
    except UserAlreadyCreatedException as e:
        raise HTTPException(status_code=400, detail=str(e))            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateUserResponse(**user.dict())   

@router.post("/login", response_model=schemas.LoginUserResponse)
def post_seller(
        login_user_req: schemas.LoginUserRequest,
        db: Session = Depends(database.get_db)):    

    try:
        user = crud.find_client(db, login_user_req)
        if user:
            user_response = user.dict()
            user_response["isOwner"] = False
            user_response["isClient"] = True
        else:
            user = crud.find_seller(db, login_user_req)
            if user is None:
                raise Exception("El usuario no existe")
            user_response = user.dict()
            user_response["isOwner"] = True
            user_response["isClient"] = False


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if login_user_req.password != user.password:
        raise HTTPException(status_code=400, detail='Passwords dont match')

    return schemas.LoginUserResponse(**user_response)

    