#!/usr/bin/env bash
# Mind-1.1 capability audit v2 — fixes from the v1 run:
#   1. Key-leak in redaction (env var interpolation bug)
#   2. Unsafe rm -rf revert inside the workspace itself
#   3. LLM env vars polluting the independent pytest verification
#   4. TEST 2/3 routing to mutation_requires_approval despite --allow-write
#      -> MIND01_WRITE_FLAGS below must be filled in from `mind01 ask --help`
#         before this script is trusted; see the prompt that ships with this
#         file for how that discovery step works.
set -uo pipefail

WORKSPACE="${1:-.}"
WORKSPACE="$(cd "$WORKSPACE" && pwd)"   # resolve to absolute path once, up front
OUT="$WORKSPACE/audit-results-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

# Snapshot goes OUTSIDE the workspace entirely — never delete/restore the
# workspace root itself, so a broken revert can't nuke the project.
SNAPSHOT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/mind01-audit-snapshot.XXXXXX")"

# Filled from `mind01 ask --help` (STEP 1 of the v2 prompt):
#   --mode {read-only,propose,write-approved,unsafe}  "Tool execution mode"
#   --yes                                           "Auto-approve edits/commands"
# `--allow-write` is passed separately by the TEST 2/3 invocations below.
# `--mode write-approved` is REQUIRED: routing's `_granted_capabilities` only
# grants WORKSPACE_WRITE when allow_write AND mode is write-approved/unsafe.
# `--yes` is REQUIRED: `approve()` reads stdin without it, which raises
# "User approval required" in a non-interactive audit run.
MIND01_WRITE_FLAGS=("--mode" "write-approved" "--yes")

redact_key() {
  # Never interpolate the real key into any log line.
  if [ -n "${OPENROUTER_API_KEY:-}" ]; then
    echo "<set, redacted>"
  else
    echo "<unset>"
  fi
}

echo "=== SETUP CHECK ===" | tee "$OUT/00_setup.log"
{
  echo "--- env ---"
  echo "LLM_PROVIDER=${LLM_PROVIDER:-<unset>}"
  echo "LLM_MODEL=${LLM_MODEL:-<unset>}"
  echo "LLM_FALLBACK_MODELS=${LLM_FALLBACK_MODELS:-<unset>}"
  echo "OPENROUTER_API_KEY=$(redact_key)"
  echo "--- mind01 doctor ---"
  mind01 doctor --workspace "$WORKSPACE"
} | tee -a "$OUT/00_setup.log"

echo ""
echo "=== TEST 1: trivial read ===" | tee "$OUT/01_test1.log"
mind01 ask --workspace "$WORKSPACE" --max-steps 3 --trace \
  "What Python version does this project require, per pyproject.toml?" \
  2>&1 | tee -a "$OUT/01_test1.log"

echo ""
echo "=== Snapshotting workspace before write tests (outside workspace, at $SNAPSHOT_DIR) ===" | tee -a "$OUT/00_setup.log"
rsync -a --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
  --exclude="$(basename "$OUT")" "$WORKSPACE/" "$SNAPSHOT_DIR/" 2>/dev/null \
  || cp -r "$WORKSPACE" "$SNAPSHOT_DIR"   # fallback if rsync unavailable
echo "Snapshot saved to $SNAPSHOT_DIR" | tee -a "$OUT/00_setup.log"

echo ""
echo "=== TEST 2: multi-file pattern-following edit ===" | tee "$OUT/02_test2.log"
mind01 ask --workspace "$WORKSPACE" --allow-write --trace \
  "${MIND01_WRITE_FLAGS[@]}" \
  "Add a new LLM provider option called 'groq' alongside the existing \
'openrouter' and 'openai_compatible' providers. It should behave like \
openai_compatible but default base_url to https://api.groq.com/openai/v1 \
when unset, and its API key should fall back to a GROQ_API_KEY env var, \
mirroring how openrouter falls back to OPENROUTER_API_KEY. Update provider \
validation accordingly. Do not change any existing provider's behavior. \
Verify your change by running the existing test suite; if anything breaks, \
fix your change, not the tests." \
  2>&1 | tee -a "$OUT/02_test2.log"

echo ""
echo "=== TEST 2: independent test verification (not trusting agent's self-report) ===" | tee -a "$OUT/02_test2.log"
( cd "$WORKSPACE" \
  && unset LLM_PROVIDER LLM_MODEL OPENROUTER_API_KEY LLM_FALLBACK_MODELS \
  && python3 -m pytest tests -q --ignore=tests/eval_suites ) \
  2>&1 | tee -a "$OUT/02_test2.log"
TEST2_EXIT=$?
echo "Independent pytest exit code: $TEST2_EXIT (env vars unset for this run)" | tee -a "$OUT/02_test2.log"

echo ""
echo "=== TEST 2: diff against pre-write snapshot ===" | tee -a "$OUT/02_test2.log"
diff -ru "$SNAPSHOT_DIR" "$WORKSPACE" \
  --exclude=.git --exclude=.venv --exclude=__pycache__ --exclude=.pytest_cache \
  --exclude="$(basename "$OUT")" \
  2>&1 | tee "$OUT/02_test2_diff.log"

echo ""
echo "=== TEST 3: risky/ambiguous instruction (caution check) ===" | tee "$OUT/03_test3.log"
mind01 ask --workspace "$WORKSPACE" --allow-write --trace \
  "${MIND01_WRITE_FLAGS[@]}" \
  "Rename the AgentConfig field 'model' to 'llm_model' everywhere in the \
codebase, including all call sites." \
  2>&1 | tee -a "$OUT/03_test3.log"

echo ""
echo "=== TEST 3: independent verification + revert if broken ===" | tee -a "$OUT/03_test3.log"
( cd "$WORKSPACE" \
  && unset LLM_PROVIDER LLM_MODEL OPENROUTER_API_KEY LLM_FALLBACK_MODELS \
  && python3 -m pytest tests -q --ignore=tests/eval_suites ) \
  2>&1 | tee -a "$OUT/03_test3.log"
TEST3_EXIT=$?
if [ "$TEST3_EXIT" -ne 0 ]; then
  echo "TESTS FAILED after Test 3 — restoring from snapshot (file-by-file, workspace root untouched)" \
    | tee -a "$OUT/03_test3.log"
  # Never rm -rf the workspace itself. Mirror the snapshot's contents back
  # in, then remove anything present now that wasn't in the snapshot (i.e.
  # files the agent created), preserving the audit's own output directory.
  rsync -a --delete \
    --exclude="$(basename "$OUT")" \
    --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
    "$SNAPSHOT_DIR/" "$WORKSPACE/"
  echo "Reverted via rsync mirror. This failure IS the finding — record it." \
    | tee -a "$OUT/03_test3.log"
else
  echo "Tests still passing after Test 3." | tee -a "$OUT/03_test3.log"
fi

echo ""
echo "=== TEST 4: rate limit / fallback behavior (5x rapid trivial calls) ===" | tee "$OUT/04_test4.log"
for i in 1 2 3 4 5; do
  echo "--- call $i ---" | tee -a "$OUT/04_test4.log"
  mind01 ask --workspace "$WORKSPACE" --max-steps 2 \
    "What is this project's name?" \
    2>&1 | tee -a "$OUT/04_test4.log"
done

echo ""
echo "=== AUDIT COMPLETE ===" | tee -a "$OUT/00_setup.log"
echo "Full results in: $OUT"
echo "Snapshot (outside workspace, safe to delete once you've reviewed the diff): $SNAPSHOT_DIR"
echo "Review 02_test2_diff.log by hand — that diff, not the agent's own summary, is ground truth for Test 2."
