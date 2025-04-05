FROM ghcr.io/astral-sh/uv:alpine



ADD . /app
WORKDIR /app
RUN uv sync --frozen


CMD ["fastapi", "dev", "--host", "0.0.0.0"]

