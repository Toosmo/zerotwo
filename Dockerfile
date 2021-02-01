FROM python:3.9.1-slim-buster as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m -r zerotwo && \
    chown zerotwo /app

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh ./
RUN chmod +x wait-for-it.sh

FROM base as builder

ARG POETRY_VERSION=1.1.4

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    git \
    python3-dev \
    && pip install --no-cache-dir poetry==$POETRY_VERSION \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock poetry.toml pyproject.toml ./

RUN poetry install --no-dev --no-root

FROM base as final

WORKDIR /app

COPY --from=builder /app/.venv .venv/

COPY . .

USER zerotwo

CMD [".venv/bin/python", "zerotwo/bot.py"]
