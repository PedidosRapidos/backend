from pedidos_rapidos.database import Seller, Shop
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_list_shops_paginated(client: TestClient, session: Session):
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=2, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=3, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=4, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=5, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=6, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=7, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=8, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=9, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=10, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Shop(id=11, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.get(
        "/shops/"
    )
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 10
