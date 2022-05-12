from pedidos_rapidos.database import Seller, Shop
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_create_shop(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.commit()

    response = client.post(
        "/sellers/1/shops/", json={"name":"ElPuestito", "address": "Calle siempre viva 123", "cbu": "00000000000000001"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None


def test_seller_list_shops_paginated(client: TestClient, session: Session):
    session.add(Seller(id=2, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=3, seller_id=2, name="Noaparece", address="NoAparece", cbu="00000000000000001" ))
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=2, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.get(
        "/sellers/1/shops/"
    )
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2
