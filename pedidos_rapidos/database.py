import os
from sqlmodel import SQLModel, create_engine, Session

from .items.models import *  # noqa: F403,F401
from .sellers.models import * # noqa: F403,F401

engine = create_engine(os.getenv("DATABASE_URL", ""))

SQLModel.metadata.create_all(engine)

metadata = SQLModel.metadata


def get_db() -> Session:
    with Session(engine) as session:
        yield session
