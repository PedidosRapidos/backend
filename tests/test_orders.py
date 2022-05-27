from pedidos_rapidos.database import (
    Cart,
    Client,
    Order,
    ProductCart,
    Seller,
    Shop,
    Product,
)
from sqlmodel import Session
from fastapi.testclient import TestClient

from pedidos_rapidos.utils.enum_utils import OrderState

# US 21
def test_get_orders_to_confirm(client: TestClient, session: Session):
    session.add(
        Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass")
    )
    session.add(
        Shop(
            id=1,
            seller_id=1,
            name="Puestito",
            address="Calle siempre viva 123",
            cbu="00000000000000001",
        )
    )
    session.add(
        Product(
            id=1,
            shop_id=1,
            name="Milanesa",
            description="Milanesa grande de carne con papas fritas",
            price=500,
            image=None,
        )
    )
    session.add(
        Client(id=1, username="ElVendedor", email="seller@mail.com", password="pass")
    )
    session.add(
        Order(
            id=1,
            client_id=1,
            state=OrderState.TO_CONFIRM,
            cart=Cart(
                id=1, products=[ProductCart(quantity=2, product_id=1)], client_id=1
            ),
        )
    )
    session.add(
        Order(
            id=2,
            client_id=1,
            state=OrderState.DELIVERED,
            cart=Cart(
                id=2, products=[ProductCart(quantity=2, product_id=1)], client_id=1
            ),
        )
    )
    session.commit()

    response = client.get("/orders?client_id=1&state=TO_CONFIRM")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == 1

# US23
def get_orders_delivered(client: TestClient, session: Session):
    session.add(
        Seller(id=1, username="ElVendedor", email="seller@mail.com", password="pass")
    )
    session.add(
        Shop(
            id=1,
            seller_id=1,
            name="Puestito",
            address="Calle siempre viva 123",
            cbu="00000000000000001",
        )
    )
    session.add(
        Product(
            id=1,
            shop_id=1,
            name="Milanesa",
            description="Milanesa grande de carne con papas fritas",
            price=500,
            image=None,
        )
    )
    session.add(
        Client(id=1, username="ElVendedor", email="seller@mail.com", password="pass")
    )
    session.add(
        Order(
            id=1,
            client_id=1,
            state=OrderState.TO_CONFIRM,
            cart=Cart(
                id=1, products=[ProductCart(quantity=2, product_id=1)], client_id=1
            ),
        )
    )
    session.add(
        Order(
            id=2,
            client_id=1,
            state=OrderState.DELIVERED,
            cart=Cart(
                id=2, products=[ProductCart(quantity=2, product_id=1)], client_id=1
            ),
        )
    )
    session.commit()

    response = client.get("/orders?client_id=1&state=DELIVERED")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == 2
