.PHONY: run test fmt

run:
	uvicorn src.api.main:app --reload --port 8000

test:
	pytest -q
