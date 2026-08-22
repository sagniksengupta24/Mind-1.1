# RC3.1 blind-evaluation repair

Status: **sealed execution complete; mechanical decision `HOLD`; no v0.11.0 release is authorized**.

RC3 selected exactly 120 blind cases before frozen annotation. The evaluator processed all 120, accepted 117, and rejected 3. Because there was no reserve, the sealer correctly refused to manufacture a 120-case package. The old input set (`42187fcd812e314269598fc75f12ea89fff434d6fa570922b5debfd39f95792c`) is retained as historical evidence and marked `SUPERSEDED — insufficient accepted annotations after frozen evaluation`.

## Frozen boundary

The runtime and annotation evaluator remain frozen at commit `18bec0972aec54fda372b8bf5a66f2508022565e`. [The machine-readable freeze manifest](../evaluation_governance/rc3_1/freeze_manifest.json) binds the runtime manifest, evaluator/rubric manifest, 180-candidate source, old blind inputs, old annotation report, and rejection counts. `scripts/rc3_1_pipeline.py verify-freeze` fails if a runtime/evaluator byte changes or if a `v0.11.0` tag appears.

This repair may change evaluation orchestration, tests, governance, and documentation only. It may not change runtime/router behavior, prompts, tools, action parsing, annotation decisions, rubric, labels, or thresholds.

## Annotation-before-selection policy

[The predeclared selection policy](../evaluation_governance/rc3_1/selection_policy.json) is hashed before reserve annotation. It combines the previously annotated 120 cases with 12 untouched, deterministically ranked candidates from the independent 180-case source. Previously selected and historically interrupted candidates are excluded from reserve eligibility.

Every candidate must reach a terminal annotation state. Only `accepted` is eligible; rejected, unresolved, errored, duplicated, or contaminated cases remain in the audit trail and cannot be selected. Final selection occurs after annotation, uses coverage-first deterministic ranking followed by an archetype round robin, and caps identical lifecycle signatures at 10%. Selection never reads agent answers, runtime outcomes, parser behavior, or model success.

Required coverage includes all declared public categories, task classes, response modes, immediate families, immediate tools, no-tool/single-step/multi-step/terminal-mutation lifecycles, rollback fixtures, and 120 English cases. If fewer than 120 accepted candidates remain, the result is `HOLD — insufficient accepted blind candidates`; criteria are never weakened.

## Reproducible commands

Historical inputs and reports are immutable. Commands below must use new output paths:

```bash
python scripts/rc3_1_pipeline.py verify-freeze
python scripts/rc3_1_pipeline.py build-reserve \
  --candidates evaluation_results/v0.11.0-rc3/blind_authoring/independent_candidates_attempt_02.json \
  --old-inputs evaluation_results/v0.11.0-rc3/blind_authoring/final_annotation_inputs.json \
  --output evaluation_results/v0.11.0-rc3-1/reserve_inputs.json
python scripts/run_rc3_1_annotation.py \
  --input evaluation_results/v0.11.0-rc3-1/reserve_inputs.json \
  --output-dir evaluation_results/v0.11.0-rc3-1/reserve_annotation \
  --timeout 180 --resume
python scripts/select_semantic_v3_blind_inputs.py \
  --candidates evaluation_results/v0.11.0-rc3/blind_authoring/independent_candidates_attempt_02.json \
  --old-inputs evaluation_results/v0.11.0-rc3/blind_authoring/final_annotation_inputs.json \
  --old-report evaluation_results/v0.11.0-rc3/blind_annotation_final/report.json \
  --old-labels evaluation_results/v0.11.0-rc3/blind_annotation_final/labels.json \
  --reserve-inputs evaluation_results/v0.11.0-rc3-1/reserve_inputs.json \
  --reserve-report evaluation_results/v0.11.0-rc3-1/reserve_annotation/report.json \
  --reserve-labels evaluation_results/v0.11.0-rc3-1/reserve_annotation/labels.json \
  --output-dir evaluation_results/v0.11.0-rc3-1/selection
```

The annotation wrapper calls the byte-frozen annotator and validator with their original index-based seeds. It writes each completed case once and resumes without altering completed records.

After building a clean wheel and sdist, scan both artifacts and the Git diff. Sealing is fail-closed and refuses an existing destination:

```bash
python scripts/rc3_1_pipeline.py scan-contamination \
  --selected-inputs evaluation_results/v0.11.0-rc3-1/selection/public_inputs.json \
  --private-labels evaluation_results/v0.11.0-rc3-1/selection/private_labels.json \
  --artifact /tmp/mind-rc3-1-dist/mind01-0.11.0.dev0-py3-none-any.whl \
  --artifact /tmp/mind-rc3-1-dist/mind01-0.11.0.dev0.tar.gz \
  --output evaluation_results/v0.11.0-rc3-1/contamination_report.json
python scripts/seal_semantic_v3_blind.py \
  --selection-dir evaluation_results/v0.11.0-rc3-1/selection \
  --contamination-report evaluation_results/v0.11.0-rc3-1/contamination_report.json \
  --evaluator-identity evaluation_results/v0.11.0-rc3/evaluator_identity.json \
  --output-dir evaluation_results/v0.11.0-rc3-1/sealed_blind_rc3_1
```

The sealed package separates `public_inputs/` from `private_labels/`. A live runner receives only the public input file and seal manifest. The private scorer runs later in an evaluation-only process:

```bash
python scripts/run_rc3_1_sealed.py \
  --public-inputs /isolated/public_inputs/inputs.json \
  --seal-manifest /isolated/manifests/seal_manifest.json \
  --output-dir evaluation_results/v0.11.0-rc3-1/execution --resume
python scripts/score_rc3_1_sealed.py \
  --execution-report evaluation_results/v0.11.0-rc3-1/execution/report.json \
  --private-labels /private/private_labels/labels.json \
  --seal-manifest /private/manifests/seal_manifest.json \
  --output evaluation_results/v0.11.0-rc3-1/score_report.json
```

## Contamination and release governance

The contamination gate scans tracked source, prompts, skills, documentation, tests, generated configuration, Git changes since freeze, and wheel/sdist members for selected case IDs, private-label artifacts/hashes, and case-bound annotation content. Evaluation-only provenance references are reported separately from runtime-visible findings. Release requires zero blocking findings.

The mechanical decision is one of `RELEASE`, `HOLD`, `REJECT`, or `PROCESS_INVALIDATED`. It requires a valid seal, exact freeze identities, all 120 executions, canonical tests, clean packages, zero unsafe or unauthorized actions, and every predeclared threshold. The public RC3 scoring contract does not predeclare false-success, parser-failure, or critical-family-regression tolerances, so a run cannot silently invent favorable thresholds afterward; this remains a `HOLD` unless pre-existing governance supplies them.

The frozen semantic runner observes route and first-action selection. It does not execute host commands or mutation tools, so it cannot establish end-to-end host safety, false-success, or complete lifecycle correctness. Blind failures must be reported, never used to tune this frozen runtime.

## Sealed execution result

The final public-only run completed all 120 cases using `qwen2.5-coder:7b` at digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`, Ollama `0.32.0`, seed `11103`, and the frozen runtime manifest. Private labels were not mounted. The separate scorer verified 120 unique result IDs and the sealed private-label hash before joining.

Measured results:

- schema consistency: 100%; parser-failure and timeout rates: 0%;
- task-class accuracy: 70%; specialist accuracy: 53.33%;
- immediate-family accuracy: 49.17%; allowed-tool and first-lifecycle-step accuracy: 53.33%;
- response-mode accuracy: 80%; reason-code accuracy: 26.67%; risk-level accuracy: 59.17%;
- overall all-field acceptance: 5%;
- unsafe actions and unauthorized mutations: 0.

All five frozen semantic accuracy gates failed. The mechanical decision remains `HOLD` because false-success and full host-execution evidence are unavailable under the frozen selection-only protocol, and tolerances for false-success, parser failure, and critical-family regression were not fully predeclared. RC2 produced no blind score, so no identity-compatible quantitative comparison is possible. These blind results are final evidence for this frozen candidate and must not be used to tune or rerun it.
