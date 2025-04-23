# ── Stage 1: build dependencies with Poetry ─────────────────────
FROM python:3.10-slim AS builder

# Install system deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry (no virtualenv creation)
ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy only pyproject and lock to install deps
COPY pyproject.toml poetry.lock* /app/

# Install runtime deps into the image
RUN /opt/poetry/bin/poetry install --no-dev

# ── Stage 2: copy code and run ─────────────────────────────────
FROM python:3.10-slim

# Copy Poetry runtime (so we can use `poetry run gateway`)
COPY --from=builder /opt/poetry /opt/poetry
ENV PATH="/opt/poetry/bin:${PATH}"

WORKDIR /app

# Copy our installed packages and source
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY src/ /app/src

# Create an empty .env file if it doesn't exist
RUN touch /app/.env

# Expose port
EXPOSE 8000

# Run the gateway
ENTRYPOINT ["poetry", "run", "gateway"]
CMD [] 