# Feature fixture

Add `normalize_identifier(text: str) -> str` to `text_utils.py`.

The function must return a deterministic lowercase ASCII identifier: trim surrounding whitespace, replace each run of non-alphanumeric characters with one underscore, collapse repeated underscores, and remove leading or trailing underscores. Preserve the existing `preserve` function.
