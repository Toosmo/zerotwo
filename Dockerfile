FROM python:3.9.0-slim-buster as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x wait-for-it.sh

FROM base as builder

RUN apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    git \
    python3-dev \
    && pip install --no-cache-dir poetry==1.1.2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock poetry.toml pyproject.toml ./

RUN poetry install --no-dev --no-root \
    && .venv/bin/python -m pip install --no-cache-dir git+https://github.com/Rapptz/discord-ext-menus

FROM base as final

WORKDIR /app

COPY --from=builder /app/.venv .venv/

COPY . .

CMD [".venv/bin/python", "zerotwo/bot.py"]
