from pedidos_rapidos.database import Seller
from pedidos_rapidos.database import Shop
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_create_product(client: TestClient, session: Session):
    session.add(Seller(id=1, email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.post(
        "/sellers/1/products/", json={"name": "Milanesa", "description": "Milanesa grande de carne con papas fritas", "price": 500, "image": "image.png"}
    )
    data = response.json()

    print(data)
    assert response.status_code == 200
    assert data["id"] is not None
