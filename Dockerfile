FROM python:3.8.2-alpine3.11 as base

ENV PYTHONUNBUFFERED=1

FROM base as builder

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    make \
    musl-dev \
    libffi \
    libffi-dev \
    openssl \
    openssl-dev \
    git \
    python3-dev \
 && pip install --no-cache-dir poetry

WORKDIR /app

COPY poetry.lock poetry.toml pyproject.toml ./

RUN poetry install --no-dev --no-root \
 && .venv/bin/python -m pip install --no-cache-dir git+https://github.com/Rapptz/discord-ext-menus \
 && apk del .build-deps

FROM base as final

WORKDIR /app

COPY --from=builder /app/.venv .venv/

COPY . .

RUN wget https://raw.githubusercontent.com/typekpb/wtfc/master/wtfc.sh \
    && chmod +x wtfc.sh

CMD [".venv/bin/python", "zerotwo/bot.py"]
