import json

import pytest

from text_recognition_core.schemas.v1 import (
    BoundaryValidationError,
    parse_request_json,
    parse_result_json,
)

REQUEST = b'{"sources":[{"source_id":"source-1"}],"mode":"OCR","languages":["en"]'


@pytest.mark.parametrize(
    "extra",
    [
        b',"privacy_mode":"LOCAL_ONLY","privacy_mode":"REMOTE_ALLOWED"',
        b',"privacy_mode":"LOCAL_ONLY","privacy_\\u006dode":"REMOTE_ALLOWED"',
        b',"context":{"secret_canary":"LOCAL_ONLY","secret_canary":"REMOTE_ALLOWED"}',
        b',"context":{"nested":{"secret_canary":1,"secret_canary":2}}',
        b',"unknown_secret_canary":1,"unknown_secret_canary":2',
    ],
)
def test_public_request_rejects_duplicate_decoded_members(extra: bytes) -> None:
    with pytest.raises(BoundaryValidationError) as caught:
        parse_request_json(REQUEST + extra + b"}")
    assert caught.value.codes == ("duplicate_json_key",)
    assert str(caught.value) == "duplicate_json_key"
    assert "secret_canary" not in str(caught.value)
    assert "REMOTE_ALLOWED" not in str(caught.value)


def _result_bytes() -> bytes:
    return json.dumps(
        {
            "document_id": "doc-1",
            "raw_result_id": "raw-1",
            "current_revision_id": "rev-1",
            "provenance": {
                "input_sha256": "a" * 64,
                "configuration_sha256": "b" * 64,
                "engine_name": "synthetic",
                "engine_version": "1",
                "model_version": "none",
                "pipeline_version": "1",
                "created_at": "2026-09-30T00:00:00Z",
                "attempt": 1,
            },
            "pages": [
                {
                    "id": "page-1",
                    "document_id": "doc-1",
                    "page_number": 1,
                    "width_px": 100,
                    "height_px": 200,
                    "regions": [],
                }
            ],
            "plain_text": "",
        }
    ).encode()


@pytest.mark.parametrize("nested", [False, True])
def test_public_result_rejects_duplicate_members(nested: bool) -> None:
    payload = _result_bytes()
    assert parse_result_json(payload).document_id == "doc-1"
    if nested:
        payload = payload.replace(
            b'"engine_version": "1"',
            b'"engine_version": "1", "engine_version": "secret_canary"',
            1,
        )
    else:
        payload = payload.replace(
            b'"document_id": "doc-1"',
            b'"document_id": "doc-1", "document_id": "secret_canary"',
            1,
        )
    with pytest.raises(BoundaryValidationError) as caught:
        parse_result_json(payload)
    assert caught.value.codes == ("duplicate_json_key",)
    assert str(caught.value) == "duplicate_json_key"


def test_valid_public_boundary_preserves_json_roundtrip() -> None:
    request = parse_request_json(REQUEST + b',"privacy_mode":"LOCAL_ONLY"}')
    assert request.privacy_mode.value == "LOCAL_ONLY"
    assert parse_request_json(request.model_dump_json().encode()) == request
    result = parse_result_json(_result_bytes())
    assert parse_result_json(result.model_dump_json().encode()) == result


@pytest.mark.parametrize(
    "payload",
    [
        b'{"secret_canary":',
        REQUEST + b',"context":{"secret_canary":' + b"9" * 5000 + b"}}",
        b'{"context":{"secret_canary":"\xff"}}',
        b'{"context":' + b"[" * 2000 + b'"secret_canary"' + b"]" * 2000 + b"}",
    ],
)
def test_public_preflight_failure_is_content_free(payload: bytes) -> None:
    with pytest.raises(BoundaryValidationError) as caught:
        parse_request_json(payload)
    assert caught.value.codes == ("json_invalid",)
    assert str(caught.value) == "json_invalid"
    assert caught.value.__suppress_context__
