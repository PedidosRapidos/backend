from ..database import Cart, Seller, Client
from sqlmodel import Session, select
from .exception import UserAlreadyCreatedException

def create_seller(
        db: Session,
        seller: Seller) -> Seller:
        
    existent_client = db.exec(select(Client).where(Client.email == seller.email)).first()
    if existent_client is not None:
        raise UserAlreadyCreatedException("Seller with that email already exists")

    existent_client = db.exec(select(Seller).where(Seller.email == seller.email)).first()
    if existent_client is not None:
        raise UserAlreadyCreatedException("Client with that email already exists")

    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller

def create_client(
        db: Session,
        client: Client) -> Client:

    existent_client = db.exec(select(Client).where(Client.email == client.email)).first()
    if existent_client is not None:
        raise UserAlreadyCreatedException("Client with that email already exists")

    existent_client = db.exec(select(Seller).where(Seller.email == client.email)).first()
    if existent_client is not None:
        raise UserAlreadyCreatedException("Client with that email already exists")
    cart = Cart(client=client)

    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart.client

def find_client(
        db: Session,
        client: Client) -> Client | None:

    return db.exec(select(Client).where(Client.email == client.email)).first()

def update_client_token(db:Session, client:Client, token:str | None ):
    if(client.token != token):
        client.token = token
        db.commit()
        db.refresh(client)

def update_seller_token(db:Session, seller:Seller, token:str | None) :
    if(seller.token != token):
        seller.token = token
        db.commit()
        db.refresh(seller)

def get_client(
        db: Session,
        client_id: int) -> Client:
    client = db.exec(select(Client).where(Client.id == client_id)).first()
    if client is None:
        raise Exception("Client does not exits")
    return client

def find_seller(
        db: Session,
        seller: Seller) -> Seller | None:

    return db.exec(select(Seller).where(Seller.email == seller.email)).first()

