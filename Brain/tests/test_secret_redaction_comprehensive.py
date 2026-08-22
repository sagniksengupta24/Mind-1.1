"""Comprehensive tests for secret detection, entropy analysis, and outbound redaction."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mind01.security import redact_secrets, redact_structure
from mind01.traces import summarize_prompt, summarize_result, TraceStore


def test_eight_categories_of_secrets_redacted() -> None:
    """Verify all 8+ real-format-but-fake secret categories are redacted."""

    # 1. AWS Access Key
    raw_aws_access = "Found AWS credential AKIAIOSFODNN7EXAMPLE in config"
    redacted_aws = redact_secrets(raw_aws_access)
    assert "AKIAIOSFODNN7EXAMPLE" not in redacted_aws
    assert "[REDACTED" in redacted_aws

    # 2. AWS Secret Key
    raw_aws_secret = "aws_secret_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'"
    redacted_secret = redact_secrets(raw_aws_secret)
    assert "wJalrXUtnFEMI" not in redacted_secret
    assert "[REDACTED" in redacted_secret

    # 3. JWT Token
    raw_jwt = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    redacted_jwt = redact_secrets(raw_jwt)
    assert "eyJhbGci" not in redacted_jwt
    assert "[REDACTED_JWT]" in redacted_jwt

    # 4. GCP API Key
    raw_gcp = "Using Google API key AIzaSyD1234567890abcdefghijklmnopqr in client"
    redacted_gcp = redact_secrets(raw_gcp)
    assert "AIzaSyD1234567890abcdefghijklmnopqr" not in redacted_gcp
    assert "[REDACTED_GCP_KEY]" in redacted_gcp

    # 5. Azure Account Key
    raw_azure = "DefaultEndpointsProtocol=https;AccountName=prod;AccountKey=dGhpcyBpcyBhIHZlcnkgc2VjcmV0IGtleSBmb3IgYXp1cmUgc3RvcmFnZQ==;EndpointSuffix=core.windows.net"
    redacted_azure = redact_secrets(raw_azure)
    assert "dGhpcyBpcyBhIHZlcnkgc2VjcmV0" not in redacted_azure
    assert "[REDACTED" in redacted_azure

    # 6. GitHub / Developer Tokens
    raw_ghp = "Authorization: token ghp_1234567890abcdefghijklmnopqrstuvwxyz12"
    redacted_ghp = redact_secrets(raw_ghp)
    assert "ghp_1234567890abcdefghijklmnopqrstuvwxyz12" not in redacted_ghp
    assert "[REDACTED_TOKEN]" in redacted_ghp

    # 7. Anthropic / LLM API Key
    raw_anthropic = "ANTHROPIC_KEY=sk-ant-api03-abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    redacted_anthropic = redact_secrets(raw_anthropic)
    assert "sk-ant-api03" not in redacted_anthropic
    assert "[REDACTED" in redacted_anthropic

    # 8. Split / Concatenated Key
    raw_concat = 'api_key = "sk-live-123456" + "7890abcdefghij"'
    redacted_concat = redact_secrets(raw_concat)
    assert "sk-live-123456" not in redacted_concat
    assert "[REDACTED" in redacted_concat

    # 9. Private Key Block
    raw_rsa = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA04...sample...fake...key...material...
-----END RSA PRIVATE KEY-----"""
    redacted_rsa = redact_secrets(raw_rsa)
    assert "sample...fake" not in redacted_rsa
    assert "[REDACTED_PRIVATE_KEY]" in redacted_rsa


def test_outbound_paths_redaction(tmp_path: Path) -> None:
    """Verify that redaction runs across logs, traces, structures, and error messages."""
    fake_token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz12"

    # Traces prompt & result summaries
    prompt_summary = summarize_prompt(f"Fix bug with token {fake_token}")
    assert fake_token not in prompt_summary["preview"]
    assert "[REDACTED" in prompt_summary["preview"]

    result_summary = summarize_result(f"Output containing {fake_token}")
    assert fake_token not in result_summary["preview"]
    assert "[REDACTED" in result_summary["preview"]

    # TraceStore event recording
    traces = TraceStore(tmp_path)
    traces.append({
        "event_type": "test_event",
        "payload": {"secret_field": fake_token, "nested": {"key": fake_token}}
    })
    daily_file = traces._daily_path()
    assert daily_file.exists()
    trace_content = daily_file.read_text(encoding="utf-8")
    assert fake_token not in trace_content
    assert "[REDACTED" in trace_content

    # Structured data
    nested_data = {
        "user": "developer",
        "keys": [fake_token, "normal_value"],
        "meta": {"token": fake_token},
    }
    cleaned = redact_structure(nested_data)
    assert fake_token not in json.dumps(cleaned)
    assert "[REDACTED" in json.dumps(cleaned)
