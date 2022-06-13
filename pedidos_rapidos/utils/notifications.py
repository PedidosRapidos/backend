import httpx
import logging

from pedidos_rapidos.database import Order, Review

logger = logging.getLogger("uvicorn")


class Notifications:
    def client_notice_order_update(self, order: Order):
        token = order.client.token
        self.notify(
            token=token,
            title=f"Your Order is now {order.state.format()}",
            body="",
            data={
                "order_id": order.id,
                "shop_id": order.shop_id,
                "state": order.state,
                "action": "order_updated",
            },
        )

    def seller_notice_order_update(self, order: Order):
        token = order.shop.seller.token
        self.notify(
            token=token,
            title=f"The client has updated the order to {order.state.format()}.",
            body="",
            data={
                "order_id": order.id,
                "shop_id": order.shop_id,
                "state": order.state,
                "action": "order_updated",
            },
        )

    def order_created(self, order: Order):
        self.notify(
            token=order.shop.seller.token,
            title="You have an order",
            body="",
            data={
                "order_id": order.id,
                "shop_id": order.shop_id,
                "action": "new_order",
            },
        )

    def product_review(self, review: Review):
        order = review.order
        self.notify(
            token=order.shop.seller.token,
            title="Your product have been reviewed",
            body="",
            data={
                "order_id": order.id,
                "seller_id": order.shop.seller_id,
                "shop_id": order.shop_id,
                "product_id": review.product_id,
                "action": "product_review",
            },
        )

    def notify(self, token: str | None, title: str, body: str, data: dict):
        if token is None:
            logger.error("User token needed for notification")
        else:
            httpx.post(
                "https://exp.host/--/api/v2/push/send",
                headers={
                    "Accept": "application/json",
                    "Accept-encoding": "gzip, deflate",
                    "Content-Type": "application/json",
                },
                json={"to": token, "title": title, "body": body, "data": data},
            )


def get_notifications() -> Notifications:
    return Notifications()
