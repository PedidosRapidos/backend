import logging
from operator import or_

from sqlmodel import Session, select, desc, asc, or_

from pedidos_rapidos.users.crud import get_client
from .schemas import ChangeOrderStateRequest, CreateOrderRequest

from ..database import CartProductCartLink, Order, Cart, Product, ProductCart, Review
from ..utils.enum_utils import OrderState

logger = logging.getLogger("uvicorn")


def create_order_from_cart(db: Session, user_id: int, req: CreateOrderRequest):

    client = get_client(db, user_id)

    cart = client.cart

    if len(cart.products) == 0:
        raise Exception("Cant make order with empty cart.")

    # Asumiendo que los productos del carrito vienen de un solo local.
    shop = cart.products[0].product.shop

    order = Order(
        cart_id=cart.id,
        state=OrderState.TO_CONFIRM,
        payment_method=req.payment_method,
        address=req.address,
        client_id=client.id,
        shop_id=shop.id,
    )
    shop.orders.append(order)

    new_cart = Cart(client_id=client.id)
    client.cart = new_cart
    db.add(order)

    db.flush()
    db.commit()
    return order


def repeat_order(db: Session, order_id: int, req: CreateOrderRequest):

    old_order = get_order(db, order_id)

    order = Order(
        cart_id=old_order.cart_id,
        state=OrderState.TO_CONFIRM,
        payment_method=req.payment_method,
        address=req.address,
        client_id=old_order.client_id,
        shop_id=old_order.shop_id,
    )

    old_order.shop.orders.append(order)

    db.add(order)
    db.flush()
    db.commit()
    return order


def review_order(db: Session, order_id: int, product_id: int, qualification: int):
    order = get_order(db=db, order_id=order_id)
    if order.state != OrderState.DELIVERED:
        raise Exception(
            "No se puede calificar un producto antes de que haya sido recibido"
        )

    existent_review = db.exec(
        select(Review)
        .where(Review.order_id == order_id)
        .where(Review.product_id == product_id)
    ).first()
    if existent_review is not None:
        raise Exception("La calificacion ya existente para ese producto")

    review = Review(
        product_id=product_id, order_id=order_id, qualification=qualification
    )

    db.add(review)
    db.flush()
    db.commit()
    db.refresh(review)
    return review


def get_order(db: Session, order_id: int):
    order = db.exec(select(Order).where(Order.id == order_id)).first()
    if order is None:
        raise Exception("Order no existe")
    return order


def get_orders(
    db: Session,
    client_id: int,
    q: str | None = None,
    states: list[str] | None = None,
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

    if states is not None:
        filter_clause = (Order.state == s for s in states)

    if q is not None:
        order_query = (
            order_query.join(Cart)
            .join(CartProductCartLink)
            .join(ProductCart)
            .join(Product)
            .group_by(Order.id)
        )
        where_clauses.append(Product.name.ilike(f"%{q}%"))
        order_query = order_query.group_by(Order.id)

    if shop_id is not None:
        where_clauses.append(Order.shop_id == shop_id)

    order_query = (
        order_query.where(*where_clauses).filter(or_(filter_clause))
        if states
        else order_query.where(*where_clauses)
    )

    if page is not None and page_size is not None:
        order_query = order_query.offset(page_size * page).limit(page_size)

    # if order_by is not None:
    #     if order == 'asc':
    #         order_query = order_query.order_by(desc(Order.), asc(Order.id))
    #     else:
    #         order_query = order_query.order_by(asc(Order.), asc(Order.id))

    return db.exec(order_query).all()


def change_state(db: Session, order_id: int, req: ChangeOrderStateRequest):

    order = db.exec(select(Order).where(Order.id == order_id)).first()

    if order is None:
        raise Exception("Order not found.")

    if req.new_state == OrderState.CANCELLED:
        if order.state != OrderState.TO_CONFIRM:
            raise Exception("Cant cancel order from actual state.")

    order.state = req.new_state

    db.flush()
    db.commit()
    return order
