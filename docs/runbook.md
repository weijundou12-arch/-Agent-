# Runbook

## Run locally
- pip install -e .
- uvicorn src.api.main:app --reload --port 8000

## Docker compose
- docker compose up --build

## Tests
- make test
