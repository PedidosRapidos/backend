import logging

from sqlmodel import Session, select, desc, asc

from pedidos_rapidos.cart.crud import get_cart
from .schemas import CreateOrderRequest

from ..database import Order, Cart, Product, ProductCart
from ..utils.enum_utils import OrderState

logger = logging.getLogger("uvicorn")


def create_order_from_cart(db: Session, cart_id: int, req: CreateOrderRequest):
    client = get_cart(db, cart_id).client
    order = Order(
        cart_id=cart_id,
        state=OrderState.TO_CONFIRM,
        payment_method=req.payment_method,
        client_id=client.id,
    )

    new_cart = Cart(client_id=client.id)
    client.cart = new_cart
    db.add(order)

    db.commit()

    db.refresh(order)
    db.refresh(client)

    return order


def get_orders(
    db: Session,
    client_id: int,
    state: str | None = None,
    shop_id: int | None = None,
    page: int | None = None,
    page_size: int | None = None,
    order: str | None = None,
    order_by: str | None = None,
) -> list[Order]:

    order_query = select(Order)

    where_clauses = []
    if client_id is not None:
        where_clauses.append(Order.client_id == client_id)

    if state is not None:
        where_clauses.append(Order.state == state)

    if shop_id is not None:
        order_query.join(Cart).join(ProductCart).join(Product)
        where_clauses.append(Product.shop_id == shop_id)

    order_query = order_query.where(*where_clauses)

    if page is not None and page_size is not None:
        order_query = order_query.offset(page_size * page).limit(page_size)

    # if order_by is not None:
    #     if order == 'asc':
    #         order_query = order_query.order_by(desc(Order.), asc(Order.id))
    #     else:
    #         order_query = order_query.order_by(asc(Order.), asc(Order.id))

    return db.exec(order_query).all()
