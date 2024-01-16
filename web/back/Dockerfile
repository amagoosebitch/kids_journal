FROM python:3.11-slim-buster
COPY pyproject.toml poetry.lock /code/

WORKDIR /code
ENV PYTHONPATH=.


RUN  pip install --no-compile --upgrade pip \
 && pip install --no-compile "poetry==1.6.1" \
 && poetry config virtualenvs.create false \
 && poetry config cache-dir /tmp/.cache/pypoetry \
 && poetry install --only main --no-interaction --no-ansi \
 && pip uninstall --yes poetry \
 && rm -rf /tmp/.cache/pypoetry \
 && rm -rf /tmp/bytecode 

COPY /db /code/db
COPY /models /code/models
COPY /src /code/src
COPY . /code

CMD [ "python3", "src/api.py"]
