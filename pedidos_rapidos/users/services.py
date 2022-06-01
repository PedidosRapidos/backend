import httpx
import logging

logger = logging.getLogger("uvicorn")


class Notifications:
    def notify(self, token: str | None, title: str, body: str, data: dict):
        raise Exception("Test not mocked")
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
