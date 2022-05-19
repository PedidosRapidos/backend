import tempfile
from io import StringIO


from pedidos_rapidos.database import Seller, Shop, Product
from sqlmodel import Session
from fastapi.testclient import TestClient

# US3
def test_create_product(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.post(
        "/sellers/1/shops/1/products",
        data={"name": "Milanesa",
                "description": "Milanesa grande de carne con papas fritas",
                "price": 500},
        files={"image": ("filename", b'Esto deberia ser una imagen en bytes', "image/jpeg")}
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
        "/products?q=Milanesa"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] is not None
    assert data[0]["name"] == "Milanesa"


# US15
def test_filter_by_price_asc_products(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Product(id=2, shop_id=1, name="Milanesa", description="Milanesa grande de carne con papas fritas", price=500, image="image.png" ))
    session.add(Product(id=3, shop_id=1, name="Salsa", description="Salsa bolognesa", price=50, image="image.png" ))
    session.add(Product(id=4, shop_id=1, name="Merengue", description="Merengue italiano con dulce de leche", price=5000, image="image.png" ))
    session.commit()

    response = client.get(
        "/products?price=asc"
    )
    data = response.json()

    assert response.status_code == 200
    assert data[0]["id"] is not None
    assert data[0]["name"] == "Salsa"


# US15
def test_filter_by_price_desc_products(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.add(Product(id=2, shop_id=1, name="Milanesa", description="Milanesa grande de carne con papas fritas", price=500, image="image.png" ))
    session.add(Product(id=3, shop_id=1, name="Salsa", description="Salsa bolognesa", price=50, image="image.png" ))
    session.add(Product(id=4, shop_id=1, name="Merengue", description="Merengue italiano con dulce de leche", price=5000, image="image.png" ))
    session.commit()

    response = client.get(
        "/products?price=desc"
    )
    data = response.json()

    assert response.status_code == 200
    assert data[0]["id"] is not None
    assert data[0]["name"] == "Merengue"


# US12
def test_modify_product(client: TestClient, session: Session):
    session.add(Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass"))
    session.add(Shop(id=1, seller_id=1, name="Puestito", address="Calle siempre viva 123", cbu="00000000000000001" ))
    session.commit()

    response = client.post(
        "/sellers/1/shops/1/products",
        data={"name": "Milanesa",
                "description": "Milanesa grande de carne con papas fritas",
                "price": 500},
        files={"image": ("filename", b'Esto deberia ser una imagen en bytes', "image/jpeg")}
    )
    data = response.json()

    response = client.put(
        f"/products/{data['id']}",
        data={"name": "Milanesota",
                "description": "Super descuento",
                "price": 499},
        files={"image": ("filename", b'Esto deberia ser una imagen en bytes', "image/jpeg")}
    )
    data = response.json()

    response_image = client.get(
        f"/products/{data['id']}/image"
    )
    assert response_image.text == 'Esto deberia ser una imagen en bytes'

    assert response.status_code == 200
    assert data["price"] == 499
    assert data["id"] is not None
