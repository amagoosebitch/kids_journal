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
	$(VENV)/bin/flake8 --jobs $(JOBS) --statistics --show-source .

pretty:
	$(VENV)/bin/isort .
	$(VENV)/bin/black .

plint: pretty lint

lint:  black-lint flake8

lock:
	$(VENV)/bin/poetry lock