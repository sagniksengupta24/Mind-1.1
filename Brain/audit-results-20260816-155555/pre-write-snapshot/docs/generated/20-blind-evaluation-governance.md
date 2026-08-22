# Blind evaluation governance

Snapshot: `3f71bd56823bbde35e70d9c57dbb858f0d1e8894` / `2026-07-30T16:25:16.739118+00:00`.

## Source-confirmed entry points

- `mind01.eval.evaluation_summary` — [mind01/eval.py:216](../../mind01/eval.py#L216)
- `mind01.eval.evaluation_metadata` — [mind01/eval.py:236](../../mind01/eval.py#L236)
- `mind01.semantic_eval.validate_external_blind_labels` — [mind01/semantic_eval.py:293](../../mind01/semantic_eval.py#L293)
- `mind01.semantic_eval._evaluation_phase` — [mind01/semantic_eval.py:357](../../mind01/semantic_eval.py#L357)
- `mind01.semantic_eval_v2._validate_blind_contract` — [mind01/semantic_eval_v2.py:315](../../mind01/semantic_eval_v2.py#L315)
- `mind01.semantic_live_eval_v2._mount_blind_labels` — [mind01/semantic_live_eval_v2.py:169](../../mind01/semantic_live_eval_v2.py#L169)
- `scripts.author_semantic_v3_blind` — [scripts/author_semantic_v3_blind.py:1](../../scripts/author_semantic_v3_blind.py#L1)
- `scripts.author_semantic_v3_blind.TOPICS` — [scripts/author_semantic_v3_blind.py:11](../../scripts/author_semantic_v3_blind.py#L11)
- `scripts.author_semantic_v3_blind.VARIANT_FRAMES` — [scripts/author_semantic_v3_blind.py:20](../../scripts/author_semantic_v3_blind.py#L20)
- `scripts.author_semantic_v3_blind.Archetype` — [scripts/author_semantic_v3_blind.py:31](../../scripts/author_semantic_v3_blind.py#L31)
- `scripts.author_semantic_v3_blind.ACTION_ARCHETYPES` — [scripts/author_semantic_v3_blind.py:50](../../scripts/author_semantic_v3_blind.py#L50)
- `scripts.author_semantic_v3_blind.NO_ACTION_ARCHETYPES` — [scripts/author_semantic_v3_blind.py:81](../../scripts/author_semantic_v3_blind.py#L81)
- `scripts.author_semantic_v3_blind.main` — [scripts/author_semantic_v3_blind.py:94](../../scripts/author_semantic_v3_blind.py#L94)
- `scripts.author_semantic_v3_blind.write_fixture` — [scripts/author_semantic_v3_blind.py:201](../../scripts/author_semantic_v3_blind.py#L201)
- `scripts.author_semantic_v3_blind.write_json` — [scripts/author_semantic_v3_blind.py:220](../../scripts/author_semantic_v3_blind.py#L220)
- `scripts.author_semantic_v3_blind.load_json` — [scripts/author_semantic_v3_blind.py:229](../../scripts/author_semantic_v3_blind.py#L229)
- `scripts.author_semantic_v3_blind.sha256` — [scripts/author_semantic_v3_blind.py:236](../../scripts/author_semantic_v3_blind.py#L236)
- `scripts.freeze_semantic_routing_v1.blind_cases` — [scripts/freeze_semantic_routing_v1.py:266](../../scripts/freeze_semantic_routing_v1.py#L266)
- `scripts.rc3_1_pipeline.GOVERNANCE` — [scripts/rc3_1_pipeline.py:18](../../scripts/rc3_1_pipeline.py#L18)
- `scripts.rc3_1_pipeline.EVALUATION_SCRIPTS` — [scripts/rc3_1_pipeline.py:33](../../scripts/rc3_1_pipeline.py#L33)
- `scripts.rc3_1_pipeline.evaluation_only_path` — [scripts/rc3_1_pipeline.py:897](../../scripts/rc3_1_pipeline.py#L897)
- `scripts.seal_semantic_v3_blind` — [scripts/seal_semantic_v3_blind.py:1](../../scripts/seal_semantic_v3_blind.py#L1)
- `scripts.seal_semantic_v3_blind.main` — [scripts/seal_semantic_v3_blind.py:10](../../scripts/seal_semantic_v3_blind.py#L10)
- `scripts.select_semantic_v3_blind_inputs` — [scripts/select_semantic_v3_blind_inputs.py:1](../../scripts/select_semantic_v3_blind_inputs.py#L1)
- `scripts.select_semantic_v3_blind_inputs.main` — [scripts/select_semantic_v3_blind_inputs.py:17](../../scripts/select_semantic_v3_blind_inputs.py#L17)
- `scripts.validate_semantic_v3_blind_independence` — [scripts/validate_semantic_v3_blind_independence.py:1](../../scripts/validate_semantic_v3_blind_independence.py#L1)
- `scripts.validate_semantic_v3_blind_independence.ROOT` — [scripts/validate_semantic_v3_blind_independence.py:15](../../scripts/validate_semantic_v3_blind_independence.py#L15)
- `scripts.validate_semantic_v3_blind_independence.EVAL_SUITES` — [scripts/validate_semantic_v3_blind_independence.py:16](../../scripts/validate_semantic_v3_blind_independence.py#L16)
- `scripts.validate_semantic_v3_blind_independence.SEQUENCE_THRESHOLD` — [scripts/validate_semantic_v3_blind_independence.py:17](../../scripts/validate_semantic_v3_blind_independence.py#L17)
- `scripts.validate_semantic_v3_blind_independence.BIGRAM_JACCARD_THRESHOLD` — [scripts/validate_semantic_v3_blind_independence.py:18](../../scripts/validate_semantic_v3_blind_independence.py#L18)
- `scripts.validate_semantic_v3_blind_independence.SEMANTIC_SIGNATURE_THRESHOLD` — [scripts/validate_semantic_v3_blind_independence.py:19](../../scripts/validate_semantic_v3_blind_independence.py#L19)
- `scripts.validate_semantic_v3_blind_independence.MINIMUM_VALIDATED` — [scripts/validate_semantic_v3_blind_independence.py:20](../../scripts/validate_semantic_v3_blind_independence.py#L20)
- `scripts.validate_semantic_v3_blind_independence.main` — [scripts/validate_semantic_v3_blind_independence.py:23](../../scripts/validate_semantic_v3_blind_independence.py#L23)
- `scripts.validate_semantic_v3_blind_independence.validate_public_case` — [scripts/validate_semantic_v3_blind_independence.py:106](../../scripts/validate_semantic_v3_blind_independence.py#L106)
- `scripts.validate_semantic_v3_blind_independence.historical_prompts` — [scripts/validate_semantic_v3_blind_independence.py:122](../../scripts/validate_semantic_v3_blind_independence.py#L122)
- `scripts.validate_semantic_v3_blind_independence.closest_duplicate` — [scripts/validate_semantic_v3_blind_independence.py:138](../../scripts/validate_semantic_v3_blind_independence.py#L138)
- `scripts.validate_semantic_v3_blind_independence.semantic_signature` — [scripts/validate_semantic_v3_blind_independence.py:170](../../scripts/validate_semantic_v3_blind_independence.py#L170)
- `scripts.validate_semantic_v3_blind_independence.semantic_similarity` — [scripts/validate_semantic_v3_blind_independence.py:192](../../scripts/validate_semantic_v3_blind_independence.py#L192)
- `scripts.validate_semantic_v3_blind_independence.STOPWORDS` — [scripts/validate_semantic_v3_blind_independence.py:201](../../scripts/validate_semantic_v3_blind_independence.py#L201)
- `scripts.validate_semantic_v3_blind_independence.normalize` — [scripts/validate_semantic_v3_blind_independence.py:207](../../scripts/validate_semantic_v3_blind_independence.py#L207)
- `scripts.validate_semantic_v3_blind_independence.token_ngrams` — [scripts/validate_semantic_v3_blind_independence.py:213](../../scripts/validate_semantic_v3_blind_independence.py#L213)
- `scripts.validate_semantic_v3_blind_independence.jaccard` — [scripts/validate_semantic_v3_blind_independence.py:218](../../scripts/validate_semantic_v3_blind_independence.py#L218)
- `scripts.validate_semantic_v3_blind_independence.load` — [scripts/validate_semantic_v3_blind_independence.py:224](../../scripts/validate_semantic_v3_blind_independence.py#L224)
- `scripts.validate_semantic_v3_blind_independence.write_json` — [scripts/validate_semantic_v3_blind_independence.py:231](../../scripts/validate_semantic_v3_blind_independence.py#L231)
- `scripts.validate_semantic_v3_blind_independence.sha256` — [scripts/validate_semantic_v3_blind_independence.py:240](../../scripts/validate_semantic_v3_blind_independence.py#L240)
- `tests.test_rc3_1_pipeline.test_untracked_evaluation_scripts_block_sealing` — [tests/test_rc3_1_pipeline.py:126](../../tests/test_rc3_1_pipeline.py#L126)
- `tests.test_semantic_routing.test_frozen_dataset_identity_and_blind_separation` — [tests/test_semantic_routing.py:271](../../tests/test_semantic_routing.py#L271)
- `tests.test_semantic_routing_v2.test_blind_is_required_only_after_external_authoring` — [tests/test_semantic_routing_v2.py:77](../../tests/test_semantic_routing_v2.py#L77)

## Scope and confidence

Statements in this generated page are source-indexed navigation. Runtime-only, model-dependent, external-process, and documentation-only behavior is not presented as source-confirmed.

## Related evidence

- [Architecture](../../.project_knowledge/architecture/system_overview.md)
- [Symbol index](../../.project_knowledge/symbols.md)
- [Source companions](source/)
