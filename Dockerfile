FROM ghcr.io/astral-sh/uv:0.13.5 AS uv
FROM python:3.13.17-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project --no-cache

COPY src ./src
COPY data/sample_acts ./data/sample_acts
RUN uv sync --locked --no-dev --no-cache
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "trade_defence_desk.api:app", "--host", "0.0.0.0", "--port", "8000"]
