# hevy-extract

Extract and fix the OpenAPI spec from [Hevy API docs](https://api.hevyapp.com/docs/) so it can be used to generate a Python SDK in `packages/api-service/`.

## How it works

The Hevy API docs page loads a `swagger-ui-init.js` script that contains the full OpenAPI spec embedded inline. Rather than parsing the JS as text, the extractor evaluates it in a sandbox with mocked Swagger UI globals (`window`, `SwaggerUIBundle`, etc.). When the script calls `SwaggerUIBundle(opts)`, the mock intercepts the call and captures `opts.spec` — the OpenAPI document. This approach is resilient to formatting changes in the script since it relies on runtime behavior, not string patterns.

After extraction, several fixes are applied to make the spec valid for `openapi-generator-cli`:

| Fix | What it does |
|-----|--------------|
| `addOperationIds` | Generates `operationId` for every endpoint that lacks one (e.g. `getWorkouts`, `postRoutines`) |
| `fixMissingParameterSchemas` | Adds `{ type: "string" }` to parameters with no `schema` |
| `fixEnumSchemaTypes` | Replaces the non-standard `type: "enum"` with `type: "string"` |
| `fixBooleanRequired` | Converts per-property `required: true` booleans into a proper `required` array on the parent object |
| `fixRefSiblings` | Wraps `$ref` nodes that have sibling properties into `allOf` so they conform to the spec |

## Role in the pipeline

This script is the first step of the code-generation pipeline orchestrated by [mise](https://mise.jdx.dev/) tasks:

```
scripts/hevy-extract/extract.ts
         │  bun run extract.ts extract -o openapi.json
         ▼
scripts/hevy-extract/openapi.json              ← raw JSON
         │  yq -p json -o yaml
         ▼
packages/api-service/openapi/hevy.openapi.yaml ← YAML spec
         │  openapi-generator-cli generate -g python
         ▼
packages/api-service/src/hevy_api_service/     ← async Python SDK
  ├── api/     (WorkoutsApi, RoutinesApi, …)
  ├── models/  (Workout, Routine, Set, …)
  └── …
```

The `mise` task `generate-models-hevy` in `packages/api-service/.mise.toml` declares a dependency on `//scripts/hevy-extract:export`, so running it will automatically fetch, fix, convert, and generate the SDK in one go.

## Prerequisites

- [Bun](https://bun.sh/) >= 1.0

## Install

```sh
bun install
```

## Usage

```sh
bun run start
```

This fetches the spec, applies all fixes, and writes it to `openapi.json`.

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--url` | `-u` | `https://api.hevyapp.com/docs/swagger-ui-init.js` | URL of the swagger-ui-init.js file |
| `--output` | `-o` | `openapi.json` | Output file path |

### Examples

```sh
# Default — extract to openapi.json
bun run start

# Custom output path
bun run extract.ts extract -o spec.json

# Custom source URL
bun run extract.ts extract -u https://example.com/swagger-ui-init.js

# Show help
bun run extract.ts extract --help
```

## Scripts

| Script | Description |
|--------|-------------|
| `bun run start` | Run the extractor |
| `bun run lint` | Type-check with `tsc --noEmit` |
| `bun run check` | Alias for `lint` |
| `bun run build` | Compile a standalone binary to `dist/hevy-extract` with bytecode + minify |

### Build

```sh
bun run build
./dist/hevy-extract extract
```

Produces a single self-contained executable using [Bun's bytecode compilation](https://bun.sh/docs/bundler/bytecode) for faster startup.
