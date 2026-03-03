# CI/CD

Three GitHub Actions workflows, all driven by [mise](https://mise.jdx.dev/).

## Workflows

| Workflow | Runs | Command |
| --- | --- | --- |
| **[lint](.github/workflows/lint.yml)** | hk check on all files + generated code drift detection | `hk check --all` |
| **[test](.github/workflows/test.yml)** | Tests in every package | `mise prepare && mise //...:test` |
| **[build](.github/workflows/build.yml)** | Docker build via remote BuildKit | `mise //packages/$project:build` |

All workflows use `jdx/mise-action` to install mise from the **same `.miserc.toml` → `.mise.tools.toml`**, which then provisions all other tools. No manual tool installation steps in CI, no version matrices, no cache configuration — the same [single source of truth](../CONTRIBUTING.md#the-core-idea-one-source-of-truth) applies here too.

## Remote Docker Builds over Tailscale

A persistent [BuildKit](https://github.com/moby/buildkit) daemon runs on a dedicated build server, reachable over [Tailscale](https://tailscale.com/). The build workflow connects directly using the buildx `remote` driver (`tcp://$HOST:$PORT`) — no SSH tunneling, no ephemeral containers.

Because the daemon is long-lived, build cache and `--mount=type=cache` layers persist across CI runs, making repeat builds significantly faster. Tailscale ACLs restrict access to the builder port to authorized machines only.

```yaml
# From build.yml
- name: Setup remote builder
  run: |
    docker buildx create \
      --name remote-builder \
      --driver remote \
      tcp://${{ secrets.REMOTE_BUILDER_ADDRESS }}:${{ secrets.REMOTE_BUILDER_PORT }}
    docker buildx use remote-builder
```

## Build → Scan → Push Gating

Every image is built locally (`docker buildx build --load`), scanned by [TruffleHog](https://github.com/trufflesecurity/trufflehog) for leaked secrets, and only pushed to the registry if the scan passes. The `--load` + separate push adds ~30-60s vs `buildx --push`, but guarantees no secret ever reaches the registry.

This is defined in the `build-push` task template in `.mise.tasks.toml`:

```
build → scan-docker (TruffleHog) → push (only if scan passes)
```

## Intelligent Image Tagging

Tags combine `GIT_SHA_SHORT` (short commit hash) + `GIT_DIFF_HASH` (SHA-1 of `git diff HEAD`). The `master` branch normalizes to `latest`. Non-alphanumeric branch characters become hyphens. This means every build — even with uncommitted local changes — gets a unique, traceable tag.

## Generated Code Drift Detection

The `generate-no-diff` job in the lint workflow re-runs all code generation (`mise "//...:generate-libs*"`), formats the output, then asserts `git status --porcelain` is empty. This catches stale generated code that someone forgot to commit.

## Security Hardening

- BuildKit secret mounts for tokens (never baked into layers)
- Non-root containers (`USER app`)
- Pinned base image digests with SHA-256
- Pinned apt package versions for reproducible builds
- Pinned GitHub Actions by commit SHA (managed by [pinact](https://github.com/suzuki-shunsuke/pinact))
- [zizmor](https://github.com/woodruffw/zizmor) static analysis for GitHub Actions workflows
- `persist-credentials: false` on all checkout steps
- Read-only `contents: read` permissions

## Local CI Simulation

Run the full CI pipeline locally with a single command:

```bash
mise all-ci    # generate → format → lint + build + test (parallel)
```
