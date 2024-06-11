PYTHON_VERSION := 3.11

VENV ?= .venv

.create-venv:
	test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install "poetry<1.6.0"

install:
	$(VENV)/bin/poetry install --only main,dev

init: .create-venv install

black-lint:
	$(VENV)/bin/black --check .

flake8:
	$(VENV)/bin/flake8 --statistics --show-source .

pretty:
	$(VENV)/bin/isort .
	$(VENV)/bin/black .

plint: pretty lint

lint:  black-lint flake8

lock:
	$(VENV)/bin/poetry lock

local-db-up:
	docker run -d --rm --name ydb-local -h localhost \
	  -p 2135:2135 -p 8765:8765 -p 2136:2136 \
	  -v $(pwd)/ydb_certs:/ydb_certs -v $(pwd)/ydb_data:/ydb_data \
	  -e YDB_DEFAULT_LOG_LEVEL=NOTICE \
	  -e GRPC_TLS_PORT=2135 -e GRPC_PORT=2136 -e MON_PORT=8765 \
	  -e YDB_USE_IN_MEMORY_PDISKS=true \
	  cr.yandex/yc/yandex-docker-local-ydb:latest
	make create-tables

create-tables:
	YDB_ANONYMOUS_CREDENTIALS=1 $(VENV)/bin/python db/create_tables.py -e grpc://localhost:2136 -d local

local-api-up:
	YDB_ANONYMOUS_CREDENTIALS=1 PYTHONPATH=. $(VENV)/bin/python src/api.py
