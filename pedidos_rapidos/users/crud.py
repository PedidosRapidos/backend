from ..database import Shop, Seller, Product, Client
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

    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def find_client(
        db: Session,
        client: Client) -> Client:

    return db.exec(select(Client).where(Client.email == client.email)).first()

def find_seller(
        db: Session,
        seller: Seller) -> Seller:

    return db.exec(select(Seller).where(Seller.email == seller.email)).first()

