import httpx

from pedidos_rapidos.database import Client, Seller

def notify_client(user: Client, title: str, body: str, data: dict):
    if user.token is None:
        raise Exception("User token needed for notification")
    httpx.post(
        "https://exp.host/--/api/v2/push/send",
        headers={
            "Accept": "application/json",
            "Accept-encoding": "gzip, deflate",
            "Content-Type": "application/json",
        },
        json={"to": user.token, "title": title, "body": body, "data": data},
    )


def notify_seller(user: Seller, title: str, body: str, data: dict):
    if user.token is None:
        raise Exception("User token needed for notification")
    httpx.post(
        "https://exp.host/--/api/v2/push/send",
        headers={
            "Accept": "application/json",
            "Accept-encoding": "gzip, deflate",
            "Content-Type": "application/json",
        },
        json={"to": user.token, "title": title, "body": body, "data": data},
    )
