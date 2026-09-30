import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from text_recognition_core.schemas.v1 import (
    BoundaryValidationError,
    RecognitionRequest,
    RecognitionResult,
    parse_request_json,
    parse_result_json,
)


@pytest.mark.parametrize("mode", ["AUTO", "OCR", "HTR", "MIXED"])
@pytest.mark.parametrize("batch_policy", ["ALL_OR_NOTHING", "ALLOW_PARTIAL"])
def test_request_modes_and_batch_policies(mode: str, batch_policy: str) -> None:
    request = RecognitionRequest.model_validate_json(
        json.dumps(
            {
                "sources": [{"source_id": "source-1"}],
                "mode": mode,
                "languages": ["uk"],
                "batch_policy": batch_policy,
            }
        )
    )
    assert request.mode == mode
    assert request.batch_policy == batch_policy
    assert RecognitionRequest.model_validate_json(request.model_dump_json()) == request


def test_request_rejects_unknown_capability_duplicate_source_and_paths() -> None:
    base = {"sources": [{"source_id": "source-1"}], "mode": "OCR", "languages": ["en"]}
    for change in (
        {"capabilities": [{"name": "INVENTED", "required": True}]},
        {"sources": [{"source_id": "source-1"}, {"source_id": "source-1"}]},
        {"sources": [{"source_id": "../etc/passwd"}]},
        {"server_path": "C:\\secret"},
        {"mode": "INVALID"},
        {"context": {"evil": object()}},
        {"context": {"deep": [[[[[[[[[1]]]]]]]]]}},
    ):
        with pytest.raises((ValidationError, TypeError)):
            RecognitionRequest.model_validate({**base, **change})


def test_request_limits_and_nonfinite_context() -> None:
    base = {"sources": [{"source_id": "source-1"}], "mode": "OCR", "languages": ["en"]}
    for change in (
        {"sources": [{"source_id": f"s-{i}"} for i in range(17)]},
        {"context": {"blob": "x" * 17000}},
        {"context": {"nan": float("nan")}},
        {"languages": ["../../etc"]},
    ):
        with pytest.raises(ValidationError):
            RecognitionRequest.model_validate({**base, **change})


def test_public_json_parser_bounds_and_redacts_bad_input() -> None:
    secret = b"PRIVATE_DOCUMENT_CONTENT"
    with pytest.raises(BoundaryValidationError) as caught:
        parse_request_json(b'{"mode":"INVALID","context":{"text":"' + secret + b'"}}')
    assert secret.decode() not in str(caught.value)
    assert caught.value.codes
    with pytest.raises(BoundaryValidationError) as caught:
        parse_request_json(b"x" * (256 * 1024 + 1))
    assert caught.value.codes == ("body_too_large_or_wrong_type",)


def test_result_hierarchy_and_raw_revision_ids() -> None:
    box = {"x": 0.1, "y": 0.1, "width": 0.2, "height": 0.2}
    result = {
        "document_id": "doc-1",
        "raw_result_id": "raw-1",
        "current_revision_id": "rev-1",
        "provenance": {
            "input_sha256": "a" * 64,
            "configuration_sha256": "b" * 64,
            "engine_name": "fake",
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
                "regions": [
                    {
                        "id": "region-1",
                        "page_id": "page-1",
                        "reading_order": 0,
                        "type": "paragraph",
                        "bbox": box,
                        "lines": [
                            {
                                "id": "line-1",
                                "region_id": "region-1",
                                "reading_order": 0,
                                "text": "hello",
                                "bbox": box,
                                "tokens": [
                                    {
                                        "id": "token-1",
                                        "line_id": "line-1",
                                        "reading_order": 0,
                                        "text": "hello",
                                        "bbox": box,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "plain_text": "hello",
    }
    parsed = RecognitionResult.model_validate_json(json.dumps(result))
    assert parsed.pages[0].regions[0].lines[0].tokens[0].text == "hello"
    assert parse_result_json(json.dumps(result).encode("utf-8")) == parsed
    with pytest.raises(ValidationError, match="raw_and_revision_ids_must_differ"):
        RecognitionResult.model_validate_json(
            json.dumps({**result, "current_revision_id": "raw-1"})
        )
    with pytest.raises(ValidationError, match="token_parent_mismatch"):
        broken = json.loads(json.dumps(result))
        broken["pages"][0]["regions"][0]["lines"][0]["tokens"][0]["line_id"] = "other"
        RecognitionResult.model_validate_json(json.dumps(broken))
    with pytest.raises(ValidationError, match="result_aggregate_limit"):
        broken = json.loads(json.dumps(result))
        broken["plain_text"] = "x" * 1_999_999
        RecognitionResult.model_validate_json(json.dumps(broken))
    with pytest.raises(ValidationError, match="provenance_timestamp_not_utc"):
        broken = json.loads(json.dumps(result))
        broken["provenance"]["created_at"] = "2026-09-30T00:00:00"
        RecognitionResult.model_validate_json(json.dumps(broken))


def test_schema_snapshot_is_generated_from_models() -> None:
    root = Path(__file__).resolve().parents[3] / "src" / "text_recognition_core" / "schemas"
    for name, model in (
        ("recognition-request-v1", RecognitionRequest),
        ("recognition-result-v1", RecognitionResult),
    ):
        expected = json.loads((root / f"{name}.schema.json").read_text(encoding="utf-8"))
        assert expected == model.model_json_schema()
