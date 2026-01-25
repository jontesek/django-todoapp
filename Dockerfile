FROM python:3.13-slim-bullseye

RUN \
    apt-get update &&\
    apt-get install -y --no-install-recommends tini && \
    pip install -U pip &&\
    pip install poetry==2.2.1 &&\
    poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .

EXPOSE 8080

USER nobody

ENTRYPOINT ["tini", "--"]
