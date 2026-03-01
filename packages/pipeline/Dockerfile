# syntax=docker/dockerfile:1.13-labs

# --- Mise binary ---
FROM jdxcode/mise:2026.2.23 AS mise

# --- Builder ---
FROM debian:trixie-slim@sha256:1d3c811171a08a5adaa4a163fbafd96b61b87aa871bbc7aa15431ac275d3d430 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.12 \
    ca-certificates=20250419 \
    curl=8.14.1-2+deb13u2 \
    git=1:2.47.3-0+deb13u1 \
    && rm -rf /var/lib/apt/lists/*

# Grab mise from its official image (not installed via apt/curl)
COPY --from=mise /usr/local/bin/mise /usr/local/bin/mise
ENV MISE_YES=1 \
    MISE_DATA_DIR=/opt/mise

# Install Python and uv via mise (versions from root .mise.toml)
WORKDIR /app
COPY .mise.toml ./
COPY packages/pipeline/.mise.toml packages/pipeline/.mise.toml

WORKDIR /app/packages/pipeline
RUN --mount=type=secret,id=GITHUB_TOKEN \
    GITHUB_TOKEN=$(cat /run/secrets/GITHUB_TOKEN 2>/dev/null || true) \
    mise install python uv \
    && cp -a "$(mise where python)" /opt/python \
    && cp -a "$(mise which uv)" /usr/local/bin/uv

ENV PATH="/opt/python/bin:$PATH"

WORKDIR /app
COPY --parents **/pyproject.toml uv.lock ./
RUN uv sync --frozen --package rp-to-strong-pipeline --no-editable
COPY packages/pipeline/src packages/pipeline/src

# --- Runtime ---
FROM debian:trixie-slim@sha256:1d3c811171a08a5adaa4a163fbafd96b61b87aa871bbc7aa15431ac275d3d430

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates=20250419 \
    libffi8=3.4.8-2 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -s /usr/sbin/nologin -d /app app

COPY --from=builder /opt/python /opt/python
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:/opt/python/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY packages/pipeline/src packages/pipeline/src


EXPOSE 3000
ENTRYPOINT ["dagster-webserver"]
CMD ["-h", "0.0.0.0", "-p", "3000"]
