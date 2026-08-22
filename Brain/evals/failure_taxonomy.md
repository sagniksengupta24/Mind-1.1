# Failure Taxonomy for Mind1.1

This document defines and classifies common failures observed during Mind1.1 evaluations.

---

## 1. Canonical JSON Failure
- **Definition**: Output is not exactly one schema-version `1.0` tool-call or final JSON object.
- **Example**: prose, XML tags, Markdown fences, or malformed JSON instead of the canonical object.
- **Severity**: High (breaks parser)
- **Likely Root Cause**: Low model adherence or high temperature configuration.
- **Recommended Fix Category**: Prompt fix / Model setting fix (lower temperature).

## 2. Structural Noise Recovery
- **Definition**: Exactly one complete, fully valid JSON object has harmless surrounding structural noise.
- **Handling**: May be extracted only after complete validation and is always recorded as `PROSE_AROUND_ACTION`; multiple objects or guessed arguments are rejected.
- **Severity**: Medium (repair incident, never a clean first-attempt success)
- **Likely Root Cause**: Pre-training bias of the base coder model.
- **Recommended Fix Category**: Prompt fix (add explicit negative constraints).

## 3. Wrong Tool Name
- **Definition**: Invoking a tool name not present in the registered schemas.
- **Example**: calling `"run_tests"` instead of allowlisted `"run_command"`.
- **Severity**: High
- **Likely Root Cause**: Weak model retention of tool docs.
- **Recommended Fix Category**: Prompt fix / Runtime code fix.

## 4. Wrong Tool Arguments
- **Definition**: Passing arguments mismatching parameter types, names, or enums.
- **Example**: passing `"path"` as an object instead of string to `"read_file"`.
- **Severity**: High
- **Likely Root Cause**: Inadequate schema documentation injection.
- **Recommended Fix Category**: Tool fix (better parameter documentation).

## 5. Hallucinated File Path
- **Definition**: Claiming operations on directories or files that do not exist.
- **Example**: trying to read `"mind01/core.py"` instead of `"mind01/agent.py"`.
- **Severity**: Medium
- **Likely Root Cause**: Guessing paths instead of exploring first.
- **Recommended Fix Category**: Prompt fix (enforce directory checks first).

## 6. Claimed File Contents Without Reading
- **Definition**: Describing code content or files without invoking search or read tools.
- **Example**: stating `"doctor.py does not check Python paths"` without executing `read_file`.
- **Severity**: High
- **Likely Root Cause**: Over-reliance on model param knowledge.
- **Recommended Fix Category**: Prompt fix (strict tool checks constraint).

## 7. Broad Unnecessary Rewrite
- **Definition**: Replacing entire file contents for minor localized modifications.
- **Example**: overwriting 500 lines using `write_file` to change a port variable.
- **Severity**: Medium (timing and storage overhead)
- **Likely Root Cause**: Inability to construct targeted diffs.
- **Recommended Fix Category**: Prompt fix (encourage `propose_edit_file`).

## 8. Missing Verification
- **Definition**: Submitting changes as successful without compiling or running test commands.
- **Example**: proposing edits to `config.py` but returning a final object without running relevant verification.
- **Severity**: Medium
- **Likely Root Cause**: Lack of validation loops inside prompt plans.
- **Recommended Fix Category**: Prompt fix (require test tool calls).

## 9. Incorrect RTL/Synthesis Claim
- **Definition**: Introducing non-synthesizable simulation statements inside logic modules.
- **Example**: using `initial #10 reset = 0;` inside a synthesizable D-FF.
- **Severity**: High (synthesis compiler failure)
- **Likely Root Cause**: Confusing testbench coding patterns with synthesizable logic styles.
- **Recommended Fix Category**: RAG fix (RTL design guidelines).

## 10. Unsafe CDC Advice
- **Definition**: Proposing single-flop synchronization for Clock Domain Crossing.
- **Example**: advising the user to synchronize multi-bit data using independent D-FF paths.
- **Severity**: High (causes hardware metastability)
- **Likely Root Cause**: Poor hardware design training.
- **Recommended Fix Category**: RAG fix / Prompt fix (CDC rules).

## 11. Bad Math Derivation
- **Definition**: Outputting mathematically incorrect variables, steps, or conclusions.
- **Example**: reversing skew sign in setup timing margins calculation.
- **Severity**: Medium
- **Likely Root Cause**: Hallucinating logic steps.
- **Recommended Fix Category**: Prompt fix (scratchpad derivation checks).

## 12. Arithmetic Hallucination
- **Definition**: Hallucinating basic addition/multiplication results.
- **Example**: stating `e^-0.1 = 0.85` instead of `0.9048`.
- **Severity**: Medium
- **Likely Root Cause**: Poor floating point arithmetic capabilities of local LLM.
- **Recommended Fix Category**: Tool fix (python calculator tool call).

## 13. Awkward Indian-Language Translation
- **Definition**: Translating syntax terms literally, making technical tutorials confusing.
- **Example**: translating `"loop compiler pointer"` to Hindi characters.
- **Severity**: Low
- **Likely Root Cause**: Literal machine translation defaults.
- **Recommended Fix Category**: Prompt fix (Vocabulary retention rules).

## 14. Storing Sensitive Memory
- **Definition**: Saving passwords, AWS keys, or API tokens into memory databases.
- **Example**: calling `remember` with a host password value.
- **Severity**: High (security credential exposure)
- **Likely Root Cause**: Blind execution of user requests.
- **Recommended Fix Category**: Prompt fix (add secrets validation rules).

## 15. Overconfident Final Answer
- **Definition**: Returning final answers with high certainty for unverified code.
- **Example**: returning a solution and claiming "tests verified" when verification failed.
- **Severity**: Medium
- **Likely Root Cause**: Model output bias.
- **Recommended Fix Category**: Prompt fix (uncertainty rules).

## 16. Max-Step Exhaustion
- **Definition**: Step limit exceeded due to parser loops or tool errors.
- **Example**: parsing error retries consuming all 8 loops before reaching a solution.
- **Severity**: Medium
- **Likely Root Cause**: Low model comprehension under failure loops.
- **Recommended Fix Category**: Model setting fix (increase max steps) / Prompt fix (error recovery).
