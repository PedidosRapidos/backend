import logging

from sqlmodel import Session, select, desc, asc

from pedidos_rapidos.cart.crud import get_cart
from .schemas import ChangeOrderStateRequest, CreateOrderRequest

from ..database import CartProductCartLink, Order, Cart, Product, ProductCart
from ..utils.enum_utils import OrderState

logger = logging.getLogger("uvicorn")


def create_order_from_cart(db: Session, cart_id: int, req: CreateOrderRequest):

    cart = get_cart(db, cart_id)

    if len(cart.products) == 0:
        raise Exception("Cant make order with empty cart.")

    # Asumiendo que los productos del carrito vienen de un solo local.
    shop = cart.products[0].product.shop

    client = cart.client

    order = Order(cart_id=cart_id, state=OrderState.TO_CONFIRM,
                  payment_method=req.payment_method, client_id=client.id, shop_id=shop.id)
    shop.orders.append(order)

    new_cart = Cart(client_id=client.id)
    client.cart = new_cart
    db.add(order)

    db.flush()
    db.commit()
    return order


def get_orders(
    db: Session,
    client_id: int,
    q: str | None = None,
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

    if shop_id is not None or q is not None:
        order_query = (
            order_query.join(Cart)
            .join(CartProductCartLink)
            .join(ProductCart)
            .join(Product)
        )

    if q is not None:
        where_clauses.append(Product.name.ilike(f"%{q}%"))

    if shop_id is not None:
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


def change_state(db: Session, order_id: int, req: ChangeOrderStateRequest):

    order = db.exec(select(Order).where(Order.id == order_id)).first()

    if req.new_state == OrderState.CANCELLED:
        if order.state != OrderState.TO_CONFIRM:
            raise Exception("Cant cancel order from actual state.")
    
    order.state = req.new_state

    db.flush()
    db.commit()
    return order