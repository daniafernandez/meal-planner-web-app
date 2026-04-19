MONGODB_URI ?= mongodb://localhost:27017
MONGODB_DB ?= meal_planner
PYTHON ?= .venv/bin/python

.PHONY: server test unit-tests

server:
	MONGODB_URI="$(MONGODB_URI)" MONGODB_DB="$(MONGODB_DB)" $(PYTHON) -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

test:
	MONGODB_URI="$(MONGODB_URI)" MONGODB_DB="$(MONGODB_DB)" $(PYTHON) -m pytest

