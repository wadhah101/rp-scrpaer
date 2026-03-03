#!/usr/bin/env bash
set -euo pipefail

# === Configuration ===
SAMPLE_SIZE="${SAMPLE_SIZE:-100}"
JOBS="${JOBS:-5}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
EVAL_DIR="$SCRIPT_DIR/ground-truths"

# === Collect all output files ===
TOTAL="$(find "$OUTPUT_DIR" -maxdepth 1 -name '*.yaml' -type f | wc -l | tr -d ' ')"

if [[ "$TOTAL" -eq 0 ]]; then
  echo "ERROR: No YAML files found in $OUTPUT_DIR" >&2
  exit 1
fi

if [[ "$SAMPLE_SIZE" -gt "$TOTAL" ]]; then
  echo "WARN: Sample size ($SAMPLE_SIZE) > total files ($TOTAL). Using all files." >&2
  SAMPLE_SIZE="$TOTAL"
fi

echo "Sampling $SAMPLE_SIZE files from $TOTAL total (jobs=$JOBS)..."

# === Pick random sample ===
SAMPLED="$(find "$OUTPUT_DIR" -maxdepth 1 -name '*.yaml' -type f | perl -MList::Util=shuffle -e 'print shuffle(<>)' | head -n "$SAMPLE_SIZE")"

# === Prepare eval output directory ===
rm -rf "$EVAL_DIR"
mkdir -p "$EVAL_DIR"

# === Export the worker function for GNU parallel ===
export EVAL_DIR
evaluate_one() {
  local file="$1"
  local filename
  filename="$(basename "$file")"

  # Parse YAML
  local rp_name
  rp_name="$(grep '^rp_embedding_name:' "$file" | sed 's/^rp_embedding_name: *//')"

  local candidates
  candidates="$(grep 'hevy_embedding_name:' "$file" | sed 's/.*hevy_embedding_name: *//')"

  # Build numbered candidate list
  local candidate_list
  candidate_list="$(echo "$candidates" | awk '{printf "  %d. %s\n", NR, $0}')"

  # Build prompt — no distances
  local prompt
  prompt="You are an expert in resistance training and exercise science.

Given an exercise from the RP (Renaissance Periodization) database, determine which candidate from the Hevy exercise database is the best match. The exercises may have different names but refer to the same or very similar movement.

RP Exercise: ${rp_name}

Hevy Candidates:
${candidate_list}

Rules:
- Pick the single best match from the candidates above.
- If NONE of the candidates are a reasonable match for the RP exercise, answer \"none\".
- Reply with ONLY a valid YAML block, nothing else. Use this exact format:

best_match: <exact candidate name or \"none\">
confidence: <high|medium|low>"

  # Call claude -p
  local response
  response="$(unset CLAUDECODE; claude -p "$prompt" --model sonnet 2>/dev/null)" || {
    echo "WARN: claude call failed for $filename" >&2
    return 1
  }

  # Clean markdown fencing
  local clean_response
  clean_response="$(echo "$response" | sed '/^```/d' | sed '/^yaml$/d')"

  local best_match confidence
  best_match="$(echo "$clean_response" | grep '^best_match:' | sed 's/^best_match: *//' | sed "s/^[\"']//" | sed "s/[\"']$//")"
  confidence="$(echo "$clean_response" | grep '^confidence:' | sed 's/^confidence: *//')"

  if [[ -z "$best_match" ]]; then
    echo "WARN: Could not parse response for $filename" >&2
    echo "Raw: $response" >&2
    return 1
  fi

  # Build candidates YAML list
  local candidates_yaml
  candidates_yaml="$(echo "$candidates" | sed 's/.*/"&"/' | sed 's/^/  - /')"

  # Write per-file result (mirrors output/ filename)
  cat > "$EVAL_DIR/$filename" <<EOF
file: ${filename}
rp_exercise: "${rp_name}"
candidates:
${candidates_yaml}
best_match: "${best_match}"
confidence: ${confidence}
EOF

  echo "OK: $filename -> $best_match ($confidence)"
}
export -f evaluate_one

# === Run in parallel ===
echo "$SAMPLED" | parallel --bar -j "$JOBS" evaluate_one {}

EVALUATED="$(find "$EVAL_DIR" -maxdepth 1 -name '*.yaml' -type f | wc -l | tr -d ' ')"
echo ""
echo "Done! Evaluated $EVALUATED / $SAMPLE_SIZE exercises."
echo "Results in: $EVAL_DIR/"
