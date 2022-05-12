from pedidos_rapidos.database import Seller, Client
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_create_seller(client: TestClient, session: Session):

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola",
            "confirmPassword": "hola",
            "isOwner": True,
            "isClient": False 
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None


def test_create_client(client: TestClient, session: Session):

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola",
            "confirmPassword": "hola",
            "isOwner": False,
            "isClient": True 
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None

def test_wrong_confirm_password_create_client(client: TestClient, session: Session):

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola1",
            "confirmPassword": "hola",
            "isOwner": False,
            "isClient": True 
        }
    )
    data = response.json()

    assert response.status_code == 400

def test_error_create_client(client: TestClient, session: Session):
    session.add(Client(id=1, username="ElVendedor", email="example@test.com", password="pass"))
    session.commit()

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola",
            "confirmPassword": "hola",
            "isOwner": False,
            "isClient": True 
        }
    )
    data = response.json()

    assert response.status_code == 400

def test_error_create_client_with_seller(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="example@test.com", password="pass"))
    session.commit()

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola",
            "confirmPassword": "hola",
            "isOwner": False,
            "isClient": True 
        }
    )
    data = response.json()

    assert response.status_code == 400

def test_error_create_seller_with_client(client: TestClient, session: Session):
    session.add(Client(id=1, username="ElVendedor", email="example@test.com", password="pass"))
    session.commit()

    response = client.post(
        "/user/register", json={
            "email": "example@test.com",
            "username": "Example",
            "password": "hola",
            "confirmPassword": "hola",
            "isOwner": True,
            "isClient": False 
        }
    )
    data = response.json()

    assert response.status_code == 400


def test_login_client(client: TestClient, session: Session):
    session.add(Client(id=1, username="ElVendedor", email="example@test.com", password="pass"))
    session.commit()

    response = client.post(
        "/user/login", json={
            "email": "example@test.com",
            "password": "pass"
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
    assert data["isClient"]


def test_login_seller(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="example@test.com", password="pass"))
    session.commit()

    response = client.post(
        "/user/login", json={
            "email": "example@test.com",
            "password": "pass"
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
    assert data["isOwner"]


def test_wrong_login_client(client: TestClient, session: Session):
    session.add(Client(id=1, username="ElVendedor", email="example@test.com", password="password"))
    session.commit()

    response = client.post(
        "/user/login", json={
            "email": "example@test.com",
            "password": "pass"
        }
    )
    data = response.json()

    assert response.status_code == 400


def test_wrong_login_seller(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="example@test.com", password="password"))
    session.commit()

    response = client.post(
        "/user/login", json={
            "email": "example@test.com",
            "password": "pass"
        }
    )
    data = response.json()

    assert response.status_code == 400
