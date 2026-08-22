# Release process

Snapshot: `3f71bd56823bbde35e70d9c57dbb858f0d1e8894` / `2026-07-30T16:25:16.739118+00:00`.

## Source-confirmed entry points

- `mind01.locking._PROCESS_LOCKS` — [mind01/locking.py:10](../../mind01/locking.py#L10)
- `mind01.locking._PROCESS_GUARD` — [mind01/locking.py:11](../../mind01/locking.py#L11)
- `mind01.rc2_complete_run._release_identity` — [mind01/rc2_complete_run.py:189](../../mind01/rc2_complete_run.py#L189)
- `scripts.build_release` — [scripts/build_release.py:1](../../scripts/build_release.py#L1)
- `scripts.build_release.ROOT` — [scripts/build_release.py:10](../../scripts/build_release.py#L10)
- `scripts.build_release._VERSION_TEXT` — [scripts/build_release.py:11](../../scripts/build_release.py#L11)
- `scripts.build_release._VERSION_MATCH` — [scripts/build_release.py:12](../../scripts/build_release.py#L12)
- `scripts.build_release.__version__` — [scripts/build_release.py:15](../../scripts/build_release.py#L15)
- `scripts.build_release.ROOT_FILES` — [scripts/build_release.py:17](../../scripts/build_release.py#L17)
- `scripts.build_release.SOURCE_DIRS` — [scripts/build_release.py:28](../../scripts/build_release.py#L28)
- `scripts.build_release.EVAL_FILES` — [scripts/build_release.py:29](../../scripts/build_release.py#L29)
- `scripts.build_release.EXCLUDED_PARTS` — [scripts/build_release.py:44](../../scripts/build_release.py#L44)
- `scripts.build_release.EXCLUDED_SUFFIXES` — [scripts/build_release.py:52](../../scripts/build_release.py#L52)
- `scripts.build_release.should_copy` — [scripts/build_release.py:55](../../scripts/build_release.py#L55)
- `scripts.build_release.copy_tree` — [scripts/build_release.py:63](../../scripts/build_release.py#L63)
- `scripts.build_release.build_release` — [scripts/build_release.py:76](../../scripts/build_release.py#L76)
- `scripts.build_release.main` — [scripts/build_release.py:105](../../scripts/build_release.py#L105)
- `scripts.finalize_v011_evidence.render_release_report` — [scripts/finalize_v011_evidence.py:242](../../scripts/finalize_v011_evidence.py#L242)
- `scripts.generate_release_evidence` — [scripts/generate_release_evidence.py:1](../../scripts/generate_release_evidence.py#L1)
- `scripts.generate_release_evidence.ROOT` — [scripts/generate_release_evidence.py:18](../../scripts/generate_release_evidence.py#L18)
- `scripts.generate_release_evidence.sha256_file` — [scripts/generate_release_evidence.py:23](../../scripts/generate_release_evidence.py#L23)
- `scripts.generate_release_evidence.run_command` — [scripts/generate_release_evidence.py:31](../../scripts/generate_release_evidence.py#L31)
- `scripts.generate_release_evidence.git_text` — [scripts/generate_release_evidence.py:65](../../scripts/generate_release_evidence.py#L65)
- `scripts.generate_release_evidence.tool_version` — [scripts/generate_release_evidence.py:72](../../scripts/generate_release_evidence.py#L72)
- `scripts.generate_release_evidence.main` — [scripts/generate_release_evidence.py:84](../../scripts/generate_release_evidence.py#L84)
- `scripts.generate_release_evidence.render_report` — [scripts/generate_release_evidence.py:245](../../scripts/generate_release_evidence.py#L245)
- `scripts.rc3_1_pipeline.release_decision` — [scripts/rc3_1_pipeline.py:806](../../scripts/rc3_1_pipeline.py#L806)
- `tests.test_release_evidence` — [tests/test_release_evidence.py:1](../../tests/test_release_evidence.py#L1)
- `tests.test_release_evidence.test_release_hash_helper_is_content_addressed` — [tests/test_release_evidence.py:11](../../tests/test_release_evidence.py#L11)
- `tests.test_release_evidence.test_release_evidence_script_is_directly_importable` — [tests/test_release_evidence.py:17](../../tests/test_release_evidence.py#L17)
- `tests.test_release_hygiene` — [tests/test_release_hygiene.py:1](../../tests/test_release_hygiene.py#L1)
- `tests.test_release_hygiene.test_version_is_centralized` — [tests/test_release_hygiene.py:16](../../tests/test_release_hygiene.py#L16)
- `tests.test_release_hygiene.test_built_artifacts_exclude_private_runtime_state` — [tests/test_release_hygiene.py:22](../../tests/test_release_hygiene.py#L22)
- `tests.test_release_hygiene.test_clean_source_release_excludes_working_state_and_history` — [tests/test_release_hygiene.py:57](../../tests/test_release_hygiene.py#L57)

## Scope and confidence

Statements in this generated page are source-indexed navigation. Runtime-only, model-dependent, external-process, and documentation-only behavior is not presented as source-confirmed.

## Related evidence

- [Architecture](../../.project_knowledge/architecture/system_overview.md)
- [Symbol index](../../.project_knowledge/symbols.md)
- [Source companions](source/)
