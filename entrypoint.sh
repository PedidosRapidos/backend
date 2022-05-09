#!/bin/bash

poetry run alembic upgrade head
poetry run uvicorn pedidos_rapidos.main:app --port $PORT --host 0.0.0.0