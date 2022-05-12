from pedidos_rapidos.database import Seller, Shop, Product
from sqlmodel import Session
from fastapi.testclient import TestClient

# US3
def test_create_product(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.post(
        "/sellers/1/shops/1/products", json={"name": "Milanesa", "description": "Milanesa grande de carne con papas fritas", "price": 500, "image": "image.png"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None


# US5
def test_view_product(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Product(id=2, shop_id=1, name="Milanesa", description="Milanesa grande de carne con papas fritas", price=500, image="image.png" ))
    session.commit()

    response = client.get(
        "/products/2"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None

# US4
def test_filter_products(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Product(id=2, shop_id=1, name="Milanesa", description="Milanesa grande de carne con papas fritas", price=500, image="image.png" ))
    session.add(Product(id=3, shop_id=1, name="Salsa", description="Salsa bolognesa", price=50, image="image.png" ))
    session.commit()

    response = client.get(
        "/products?name=Milanesa"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] is not None
    assert data[0]["name"] == "Milanesa"
