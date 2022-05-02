FROM python:3.10

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /opt/app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-interaction

COPY . .

ENTRYPOINT poetry run alembic upgrade head && poetry uvicorn pedidos_rapidos.main:app --port $PORT --host 0.0.0.0
