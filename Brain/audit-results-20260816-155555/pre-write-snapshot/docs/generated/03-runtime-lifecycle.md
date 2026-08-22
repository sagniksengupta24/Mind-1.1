# Runtime lifecycle

Snapshot: `3f71bd56823bbde35e70d9c57dbb858f0d1e8894` / `2026-07-30T16:25:16.739118+00:00`.

## Source-confirmed entry points

- `mind01.agent._build_runtime_context` — [mind01/agent.py:692](../../mind01/agent.py#L692)
- `mind01.agent._runtime_completion_decision` — [mind01/agent.py:817](../../mind01/agent.py#L817)
- `mind01.agent._runtime_completion_status` — [mind01/agent.py:849](../../mind01/agent.py#L849)
- `mind01.annotation_v3._validate_lifecycle` — [mind01/annotation_v3.py:679](../../mind01/annotation_v3.py#L679)
- `mind01.annotation_v3._lifecycle_payload` — [mind01/annotation_v3.py:695](../../mind01/annotation_v3.py#L695)
- `mind01.annotation_v3._lifecycle_signature` — [mind01/annotation_v3.py:704](../../mind01/annotation_v3.py#L704)
- `mind01.file_safety.RUNTIME_DIR` — [mind01/file_safety.py:8](../../mind01/file_safety.py#L8)
- `mind01.file_safety.SENSITIVE_RUNTIME_SUFFIXES` — [mind01/file_safety.py:9](../../mind01/file_safety.py#L9)
- `mind01.file_safety.is_runtime_path` — [mind01/file_safety.py:51](../../mind01/file_safety.py#L51)
- `mind01.file_safety.ensure_not_runtime_path` — [mind01/file_safety.py:59](../../mind01/file_safety.py#L59)
- `mind01.semantic_eval.MUTATING_RUNTIME_TOOLS` — [mind01/semantic_eval.py:45](../../mind01/semantic_eval.py#L45)
- `mind01.semantic_router_v2.FirstLifecycleStep` — [mind01/semantic_router_v2.py:77](../../mind01/semantic_router_v2.py#L77)
- `mind01.semantic_router_v2.FAMILY_LIFECYCLE` — [mind01/semantic_router_v2.py:793](../../mind01/semantic_router_v2.py#L793)
- `mind01.semantic_router_v2.resolve_lifecycle` — [mind01/semantic_router_v2.py:1735](../../mind01/semantic_router_v2.py#L1735)
- `mind01.tool_exposure.LifecyclePhase` — [mind01/tool_exposure.py:14](../../mind01/tool_exposure.py#L14)
- `scripts.freeze_semantic_routing_v2.lifecycle_step` — [scripts/freeze_semantic_routing_v2.py:103](../../scripts/freeze_semantic_routing_v2.py#L103)
- `scripts.freeze_semantic_routing_v2.lifecycle_cases` — [scripts/freeze_semantic_routing_v2.py:240](../../scripts/freeze_semantic_routing_v2.py#L240)
- `scripts.rc3_1_pipeline.runtime_manifest` — [scripts/rc3_1_pipeline.py:177](../../scripts/rc3_1_pipeline.py#L177)
- `scripts.rc3_1_pipeline.lifecycle_signature` — [scripts/rc3_1_pipeline.py:877](../../scripts/rc3_1_pipeline.py#L877)
- `tests.test_action_reliability.test_every_visible_schema_matches_runtime_validation` — [tests/test_action_reliability.py:49](../../tests/test_action_reliability.py#L49)
- `tests.test_action_reliability.test_runtime_downgrades_verified_without_evidence` — [tests/test_action_reliability.py:79](../../tests/test_action_reliability.py#L79)
- `tests.test_action_reliability.test_runtime_accepts_verified_with_referenced_evidence` — [tests/test_action_reliability.py:85](../../tests/test_action_reliability.py#L85)
- `tests.test_rc2_complete_run.test_complete_run_gate_keeps_selection_lifecycle_execution_and_truth_separate` — [tests/test_rc2_complete_run.py:6](../../tests/test_rc2_complete_run.py#L6)
- `tests.test_rc3_1_pipeline.test_runtime_source_drift_blocks_freeze` — [tests/test_rc3_1_pipeline.py:143](../../tests/test_rc3_1_pipeline.py#L143)
- `tests.test_rc3_1_pipeline.test_private_labels_absent_from_runtime_artifact` — [tests/test_rc3_1_pipeline.py:159](../../tests/test_rc3_1_pipeline.py#L159)
- `tests.test_release_hygiene.test_built_artifacts_exclude_private_runtime_state` — [tests/test_release_hygiene.py:22](../../tests/test_release_hygiene.py#L22)
- `tests.test_routed_execution.test_empty_discovery_does_not_advance_lifecycle` — [tests/test_routed_execution.py:126](../../tests/test_routed_execution.py#L126)
- `tests.test_semantic_router_v2.test_lifecycle_never_mutates_before_inspection` — [tests/test_semantic_router_v2.py:115](../../tests/test_semantic_router_v2.py#L115)
- `tests.test_semantic_router_v2.test_v2_feature_flag_and_comparison_mode_preserve_runtime_contract` — [tests/test_semantic_router_v2.py:341](../../tests/test_semantic_router_v2.py#L341)

## Scope and confidence

Statements in this generated page are source-indexed navigation. Runtime-only, model-dependent, external-process, and documentation-only behavior is not presented as source-confirmed.

## Related evidence

- [Architecture](../../.project_knowledge/architecture/system_overview.md)
- [Symbol index](../../.project_knowledge/symbols.md)
- [Source companions](source/)
