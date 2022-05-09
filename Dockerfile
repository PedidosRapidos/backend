FROM python:3.10

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /opt/app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-interaction

COPY . .

CMD ["bash", "entrypoint.sh"]
