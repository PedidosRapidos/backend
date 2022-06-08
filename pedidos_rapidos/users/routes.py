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
def post_register_seller(
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
def post_login_seller(
        login_user_req: schemas.LoginUserRequest,
        db: Session = Depends(database.get_db)):    

    try:
        user = crud.find_client(db, login_user_req)
        if user:
            crud.update_client_token(db, user, login_user_req.token)
            user_response = user.dict()
            user_response["isOwner"] = False
            user_response["isClient"] = True
            if user.cart is not None:
                user_response["cartId"] = user.cart.id
        else:
            user = crud.find_seller(db, login_user_req)
            if user is None:
                raise Exception("El usuario no existe")
            crud.update_seller_token(db, user, login_user_req.token)
            user_response = user.dict()
            user_response["isOwner"] = True
            user_response["isClient"] = False

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if login_user_req.password != user.password:
        raise HTTPException(status_code=400, detail='Passwords dont match')

    return schemas.LoginUserResponse(**user_response)

@router.post("/refresh", response_model=schemas.LoginUserResponse)
def refresh_login(
        login_user_req: schemas.LoginRefresh,
        db: Session = Depends(database.get_db)):

    try:
        user = crud.find_client_by_email(db, login_user_req.email)
        if user:
            crud.update_client_token(db, user, login_user_req.token)
            user_response = user.dict()
            user_response["isOwner"] = False
            user_response["isClient"] = True
            if user.cart is not None:
                user_response["cartId"] = user.cart.id
        else:
            user = crud.find_seller_by_email(db, login_user_req.email)
            if user is None:
                raise Exception("El usuario no existe")
            crud.update_seller_token(db, user, login_user_req.token)
            user_response = user.dict()
            user_response["isOwner"] = True
            user_response["isClient"] = False

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return schemas.LoginUserResponse(**user_response)

@router.post("/logout")
def post_logout_seller(
        req: schemas.LogoutUserRequest,
        db: Session = Depends(database.get_db)):
    try:
        user = crud.find_client_by_email(db, req.email)
        if user:
            crud.update_client_token(db, user, None)
            return None

        user = crud.find_seller_by_email(db, req.email)
        if user:
            crud.update_seller_token(db, user, None)
            return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user( 
        user_id: int,
        db: Session = Depends(database.get_db) ):

    try:
        user = crud.get_client(db, client_id=user_id)
        user_response = user.dict()
        user_response["cartId"] = user.cart.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.UserResponse(**user_response)
