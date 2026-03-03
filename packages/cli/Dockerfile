# syntax=docker/dockerfile:1.13-labs
FROM jdxcode/mise:2026.2.23 AS mise

FROM debian:trixie-slim@sha256:1d3c811171a08a5adaa4a163fbafd96b61b87aa871bbc7aa15431ac275d3d430 AS builder

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.12 \
    ca-certificates=20250419 \
    curl=8.14.1-2+deb13u2 \
    git=1:2.47.3-0+deb13u1

COPY --from=mise /usr/local/bin/mise /usr/local/bin/mise
ENV MISE_YES=1 \
    MISE_DATA_DIR=/opt/mise

WORKDIR /app
COPY .miserc.toml .mise.env.toml .mise.tools.toml ./
COPY packages/cli/.mise.toml packages/cli/.mise.toml

WORKDIR /app/packages/cli
RUN --mount=type=secret,id=GITHUB_TOKEN \
    GITHUB_TOKEN=$(cat /run/secrets/GITHUB_TOKEN 2>/dev/null || true) \
    mise install python uv \
    && cp -a "$(mise where python)" /opt/python \
    && cp -a "$(mise which uv)" /usr/local/bin/uv

ENV PATH="/opt/python/bin:$PATH"

WORKDIR /app
COPY --parents **/pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package rp-to-hevy-cli --no-editable --compile-bytecode

FROM debian:trixie-slim@sha256:1d3c811171a08a5adaa4a163fbafd96b61b87aa871bbc7aa15431ac275d3d430

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates=20250419 \
    libffi8=3.4.8-2 \
    && useradd -r -s /usr/sbin/nologin -d /app app

COPY --from=builder /opt/python /opt/python
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:/opt/python/bin:$PATH" \
    PYTHONPATH="/app/packages:/app/.venv" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

COPY packages/cli/src packages/api-service/src packages/embeddings/src /app/packages/

WORKDIR /app/packages
CMD ["python", "rp_to_hevy_cli/__main__.py"]
