from pedidos_rapidos.database import Seller
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_create_shop(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.commit()

    response = client.post(
        "/sellers/1/shops/", json={"address": "Calle siempre viva 123", "cbu": "00000000000000001"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
