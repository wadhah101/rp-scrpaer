#!/usr/bin/env bash
set -euo pipefail

BUILDKIT_VERSION="v0.21.1"
BUILDKIT_USER="docker-builder"
SOCKET_PATH="/run/buildkit/buildkitd.sock"

# ── Install buildkitd ────────────────────────────────────────────────
if ! command -v buildkitd &>/dev/null; then
  echo "Installing BuildKit ${BUILDKIT_VERSION}…"
  ARCH=$(uname -m)
  case "$ARCH" in
    x86_64)  ARCH=amd64 ;;
    aarch64) ARCH=arm64 ;;
    *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;;
  esac
  curl -fsSL "https://github.com/moby/buildkit/releases/download/${BUILDKIT_VERSION}/buildkit-${BUILDKIT_VERSION}.linux-${ARCH}.tar.gz" \
    | tar -xz -C /usr/local
else
  echo "buildkitd already installed: $(buildkitd --version)"
fi

# ── QEMU binfmt for cross-platform builds ─────────────────────────────
if ! test -f /proc/sys/fs/binfmt_misc/qemu-aarch64; then
  echo "Registering QEMU binfmt for arm64…"
  docker run --privileged --rm tonistiigi/binfmt --install arm64
fi

# ── Config ────────────────────────────────────────────────────────────
mkdir -p /etc/buildkit
cat > /etc/buildkit/buildkitd.toml <<'TOML'
[worker.oci]
  platforms = ["linux/amd64", "linux/arm64"]
  gc = true
  gckeepBytes = 5_000_000_000     # 5 GB reserved
  [[worker.oci.gcpolicy]]
    keepBytes = 5_000_000_000
    keepDuration = 604800          # 7 days
    filters = ["type==regular"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 10_000_000_000     # hard cap 10 GB
TOML

# ── systemd service ──────────────────────────────────────────────────
cat > /etc/systemd/system/buildkit.service <<EOF
[Unit]
Description=BuildKit daemon
After=network.target

[Service]
ExecStart=/usr/local/bin/buildkitd \\
  --addr unix://${SOCKET_PATH} \\
  --addr tcp://0.0.0.0:1234 \\
  --group ${BUILDKIT_USER} \\
  --config /etc/buildkit/buildkitd.toml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now buildkit.service

echo "BuildKit is running:"
systemctl status buildkit.service --no-pager
