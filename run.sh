#!/bin/bash

docker run -d \
  --name shortner-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=shortner \
  -p 5432:5432 \
  postgres:15

sleep 3

python -m alembic upgrade head

python app.py
