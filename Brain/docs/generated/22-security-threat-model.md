# Security threat model

Snapshot: `3f71bd56823bbde35e70d9c57dbb858f0d1e8894` / `2026-07-30T16:25:16.739118+00:00`.

## Source-confirmed entry points

- `mind01.action_parser.MAX_MODEL_OUTPUT_CHARS` — [mind01/action_parser.py:14](../../mind01/action_parser.py#L14)
- `mind01.agent._model_phase` — [mind01/agent.py:778](../../mind01/agent.py#L778)
- `mind01.agent.preview_model_output` — [mind01/agent.py:945](../../mind01/agent.py#L945)
- `mind01.doctor.extract_model_names` — [mind01/doctor.py:81](../../mind01/doctor.py#L81)
- `mind01.end_to_end_eval.EXPECTED_MODEL_DIGEST` — [mind01/end_to_end_eval.py:25](../../mind01/end_to_end_eval.py#L25)
- `mind01.llm.OllamaClient.model_metadata` — [mind01/llm.py:38](../../mind01/llm.py#L38)
- `mind01.rc2_complete_run._require_consistent_model_identity` — [mind01/rc2_complete_run.py:214](../../mind01/rc2_complete_run.py#L214)
- `mind01.security` — [mind01/security.py:1](../../mind01/security.py#L1)
- `mind01.security.SECRET_PATTERNS` — [mind01/security.py:6](../../mind01/security.py#L6)
- `mind01.security.redact_secrets` — [mind01/security.py:13](../../mind01/security.py#L13)
- `mind01.semantic_benchmark_v2.policy_overrode_model` — [mind01/semantic_benchmark_v2.py:601](../../mind01/semantic_benchmark_v2.py#L601)
- `mind01.semantic_live_eval_v2.EXPECTED_MODEL_DIGEST` — [mind01/semantic_live_eval_v2.py:26](../../mind01/semantic_live_eval_v2.py#L26)
- `mind01.semantic_router_v2.ModelCallStats` — [mind01/semantic_router_v2.py:212](../../mind01/semantic_router_v2.py#L212)
- `mind01.semantic_router_v2.ModelCallStats.to_dict` — [mind01/semantic_router_v2.py:221](../../mind01/semantic_router_v2.py#L221)
- `scripts.freeze_semantic_v3_evaluator.EXPECTED_MODEL` — [scripts/freeze_semantic_v3_evaluator.py:18](../../scripts/freeze_semantic_v3_evaluator.py#L18)
- `scripts.freeze_semantic_v3_evaluator.live_model_identity` — [scripts/freeze_semantic_v3_evaluator.py:117](../../scripts/freeze_semantic_v3_evaluator.py#L117)
- `scripts.run_rc3_1_sealed.EXPECTED_MODEL_DIGEST` — [scripts/run_rc3_1_sealed.py:29](../../scripts/run_rc3_1_sealed.py#L29)
- `scripts.run_semantic_v3_annotation.MODEL` — [scripts/run_semantic_v3_annotation.py:25](../../scripts/run_semantic_v3_annotation.py#L25)
- `scripts.run_semantic_v3_annotation.MODEL_DIGEST` — [scripts/run_semantic_v3_annotation.py:26](../../scripts/run_semantic_v3_annotation.py#L26)
- `scripts.run_semantic_v3_annotation.model_identity` — [scripts/run_semantic_v3_annotation.py:206](../../scripts/run_semantic_v3_annotation.py#L206)
- `tests.test_action_reliability.test_ollama_missing_model_404_is_reported_as_missing_model` — [tests/test_action_reliability.py:106](../../tests/test_action_reliability.py#L106)
- `tests.test_api.test_api_security_and_sessions` — [tests/test_api.py:236](../../tests/test_api.py#L236)
- `tests.test_semantic_router_v2.test_model_policy_and_execution_family_disagreements_are_bounded` — [tests/test_semantic_router_v2.py:220](../../tests/test_semantic_router_v2.py#L220)
- `tests.test_semantic_router_v2.test_model_classifier_normal_budget_and_bounded_repair` — [tests/test_semantic_router_v2.py:402](../../tests/test_semantic_router_v2.py#L402)
- `tests.test_semantic_router_v2.test_model_classifier_repair_exhaustion_and_timeout_fall_back_safely` — [tests/test_semantic_router_v2.py:421](../../tests/test_semantic_router_v2.py#L421)

## Scope and confidence

Statements in this generated page are source-indexed navigation. Runtime-only, model-dependent, external-process, and documentation-only behavior is not presented as source-confirmed.

## Related evidence

- [Architecture](../../.project_knowledge/architecture/system_overview.md)
- [Symbol index](../../.project_knowledge/symbols.md)
- [Source companions](source/)
