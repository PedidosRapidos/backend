import json

from pedidos_rapidos.database import Cart, Seller, Shop, Product
from sqlmodel import Session
from fastapi.testclient import TestClient


def test_create_shop(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Product(id=2, shop_id=1, name="Milanesa", description="Milanesa grande de carne con papas fritas", price=500 ))
    session.commit()

    response = client.post(
        "/shopping_cart/", json={"products": [
            {
                "id": 2,
                "price": 500,
                "name": "Milanesa",
                "description": "Milanesa grande de carne con papas fritas",
                "image": "image.png",
                "shop_id": 1
            },
        ]
        }
    )

    data = response.json()
    assert response.status_code == 200
    assert data["id"] is not None
