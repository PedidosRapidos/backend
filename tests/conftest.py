import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from fastapi.testclient import TestClient
from pedidos_rapidos.app import app
from pedidos_rapidos.database import get_db
from pedidos_rapidos.utils.notifications import Notifications, get_notifications


@pytest.fixture(name="notifications")
def notifications_fixture():
    class NotificationsMock(Notifications):
        def notify(self, token: str | None, title: str, body: str, data: dict):
            print("notified", token, title, body, data)

    return NotificationsMock()


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session, notifications: Notifications):
    def get_session_override():
        return session

    def get_notifications_override():
        return notifications

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_notifications] = get_notifications_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
