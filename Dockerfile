FROM ghcr.io/astral-sh/uv:debian-slim


ADD . /app
WORKDIR /app
RUN uv sync --frozen

CMD ["uv", "run", "uvicorn","app.main:app","--host", "0.0.0.0","--port","8080"]

