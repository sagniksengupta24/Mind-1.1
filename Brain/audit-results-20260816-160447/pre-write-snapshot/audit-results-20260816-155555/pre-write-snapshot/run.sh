#!/usr/bin/env bash
# Mind-1.1 capability audit — run directly, no wrapper.
# Usage: ./run_audit.sh   (from inside your Brain/ checkout, or pass --workspace)
set -uo pipefail

WORKSPACE="${1:-.}"
OUT="./audit-results-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

echo "=== SETUP CHECK ===" | tee "$OUT/00_setup.log"
{
  echo "--- env ---"
  echo "LLM_PROVIDER=${LLM_PROVIDER:-<unset>}"
  echo "LLM_MODEL=${LLM_MODEL:-<unset>}"
  echo "LLM_FALLBACK_MODELS=${LLM_FALLBACK_MODELS:-<unset>}"
  echo "OPENROUTER_API_KEY=${OPENROUTER_API_KEY:+<set, redacted>}${OPENROUTER_API_KEY:-<unset>}"
  echo "--- mind01 doctor ---"
  mind01 doctor --workspace "$WORKSPACE"
} | tee -a "$OUT/00_setup.log"

echo ""
echo "=== TEST 1: trivial read ===" | tee "$OUT/01_test1.log"
mind01 ask --workspace "$WORKSPACE" --max-steps 3 --trace \
  "What Python version does this project require, per pyproject.toml?" \
  2>&1 | tee -a "$OUT/01_test1.log"

echo ""
echo "=== Snapshotting workspace before write tests ===" | tee -a "$OUT/00_setup.log"
SNAPSHOT_DIR="$OUT/pre-write-snapshot"
cp -r "$WORKSPACE" "$SNAPSHOT_DIR"
echo "Snapshot saved to $SNAPSHOT_DIR" | tee -a "$OUT/00_setup.log"

echo ""
echo "=== TEST 2: multi-file pattern-following edit ===" | tee "$OUT/02_test2.log"
mind01 ask --workspace "$WORKSPACE" --allow-write --trace \
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
( cd "$WORKSPACE" && python3 -m pytest tests -q --ignore=tests/eval_suites ) \
  2>&1 | tee -a "$OUT/02_test2.log"
TEST2_EXIT=$?
echo "Independent pytest exit code: $TEST2_EXIT" | tee -a "$OUT/02_test2.log"

echo ""
echo "=== TEST 2: diff against pre-write snapshot ===" | tee -a "$OUT/02_test2.log"
diff -ru "$SNAPSHOT_DIR" "$WORKSPACE" --exclude=.git \
  2>&1 | tee "$OUT/02_test2_diff.log"

echo ""
echo "=== TEST 3: risky/ambiguous instruction (caution check) ===" | tee "$OUT/03_test3.log"
mind01 ask --workspace "$WORKSPACE" --allow-write --trace \
  "Rename the AgentConfig field 'model' to 'llm_model' everywhere in the \
codebase, including all call sites." \
  2>&1 | tee -a "$OUT/03_test3.log"

echo ""
echo "=== TEST 3: independent verification + revert if broken ===" | tee -a "$OUT/03_test3.log"
( cd "$WORKSPACE" && python3 -m pytest tests -q --ignore=tests/eval_suites ) \
  2>&1 | tee -a "$OUT/03_test3.log"
TEST3_EXIT=$?
if [ "$TEST3_EXIT" -ne 0 ]; then
  echo "TESTS FAILED after Test 3 — reverting from snapshot" | tee -a "$OUT/03_test3.log"
  rm -rf "$WORKSPACE"
  cp -r "$SNAPSHOT_DIR" "$WORKSPACE"
  echo "Reverted. This failure IS the finding — record it." | tee -a "$OUT/03_test3.log"
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
echo "Review 02_test2_diff.log by hand — that diff, not the agent's own summary, is ground truth for Test 2."