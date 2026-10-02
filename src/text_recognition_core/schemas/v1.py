"""Strict RecognitionRequest/Result v1 boundary. Domain stays Pydantic-free."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from enum import StrEnum
from math import isfinite
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    ValidationError,
    field_validator,
    model_validator,
)

from text_recognition_core.domain.values import BatchPolicy, PrivacyMode, RecognitionMode

MAX_SOURCES = 16
MAX_PAGES = 256
MAX_REGIONS = 4096
MAX_LINES = 4096
MAX_TOKENS = 8192
MAX_CONTEXT_BYTES = 16 * 1024
MAX_JSON_DEPTH = 8
MAX_JSON_ITEMS = 256
MAX_TOTAL_REGIONS = 4096
MAX_TOTAL_LINES = 16384
MAX_TOTAL_TOKENS = 65536
MAX_RESULT_TEXT_CHARS = 2_000_000
MAX_REQUEST_JSON_BYTES = 256 * 1024
MAX_RESULT_JSON_BYTES = 8 * 1024 * 1024
Id = str


def _check_id(value: str) -> str:
    from text_recognition_core.domain.values import StableId

    return StableId(value).value


def _unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate_{label}")


def _json_value(value: Any, depth: int, budget: list[int]) -> None:
    budget[0] -= 1
    if budget[0] < 0 or depth > MAX_JSON_DEPTH:
        raise ValueError("context_json_limit")
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float) and isfinite(value):
        return
    if isinstance(value, list):
        for item in value:
            _json_value(item, depth + 1, budget)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for item in value.values():
            _json_value(item, depth + 1, budget)
        return
    raise ValueError("context_not_json")


class Boundary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, allow_inf_nan=False)


class CapabilityName(StrEnum):
    TEXT = "TEXT"
    LAYOUT = "LAYOUT"
    TABLES = "TABLES"
    HANDWRITING = "HANDWRITING"
    RECEIPT = "RECEIPT"
    MATH = "MATH"
    CHECKBOXES = "CHECKBOXES"
    BARCODES = "BARCODES"


class SourceRef(Boundary):
    source_id: StrictStr = Field(min_length=1, max_length=128)

    @field_validator("source_id")
    @classmethod
    def valid_id(cls, value: str) -> str:
        return _check_id(value)


class CapabilityRequirement(Boundary):
    name: CapabilityName
    required: StrictBool = True


class PreprocessingOptions(Boundary):
    deskew: StrictBool = False
    denoise: StrictBool = False


class EnginePreferences(Boundary):
    preferred: tuple[StrictStr, ...] = Field(default=(), max_length=8)


class OutputOptions(Boundary):
    include_layout: StrictBool = True
    include_alternatives: StrictBool = True


class RecognitionRequest(Boundary):
    schema_version: str = Field(
        default="recognition-request/v1", pattern=r"^recognition-request/v1$"
    )
    sources: tuple[SourceRef, ...] = Field(min_length=1, max_length=MAX_SOURCES)
    batch_policy: BatchPolicy = BatchPolicy.ALL_OR_NOTHING
    mode: RecognitionMode
    languages: tuple[StrictStr, ...] = Field(min_length=1, max_length=16)
    capabilities: tuple[CapabilityRequirement, ...] = Field(default=(), max_length=16)
    privacy_mode: PrivacyMode = PrivacyMode.LOCAL_ONLY
    preprocessing: PreprocessingOptions = Field(default_factory=PreprocessingOptions)
    engine_preferences: EnginePreferences = Field(default_factory=EnginePreferences)
    output: OutputOptions = Field(default_factory=OutputOptions)
    context: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: StrictStr | None = Field(default=None, min_length=1, max_length=128)

    @field_validator("context")
    @classmethod
    def bounded_context(cls, value: dict[str, Any]) -> dict[str, Any]:
        _json_value(value, 0, [MAX_JSON_ITEMS])
        if (
            len(json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8"))
            > MAX_CONTEXT_BYTES
        ):
            raise ValueError("context_too_large")
        return value

    @model_validator(mode="after")
    def unique_sources(self) -> Self:
        _unique([source.source_id for source in self.sources], "source_id")
        _unique([cap.name for cap in self.capabilities], "capability")
        if any(
            not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", language)
            for language in self.languages
        ):
            raise ValueError("invalid_language_tag")
        return self


class NormalizedBox(Boundary):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)

    @model_validator(mode="after")
    def inside_page(self) -> Self:
        if self.x + self.width > 1 or self.y + self.height > 1:
            raise ValueError("bbox_outside_page")
        return self


class AlternativeResult(Boundary):
    text: StrictStr = Field(max_length=4096)
    confidence: float = Field(ge=0, le=1)


class TokenResult(Boundary):
    id: StrictStr
    line_id: StrictStr
    reading_order: int = Field(ge=0)
    text: StrictStr = Field(max_length=4096)
    bbox: NormalizedBox
    confidence: float | None = Field(default=None, ge=0, le=1)
    alternatives: tuple[AlternativeResult, ...] = Field(default=(), max_length=16)


class LineResult(Boundary):
    id: StrictStr
    region_id: StrictStr
    reading_order: int = Field(ge=0)
    text: StrictStr = Field(max_length=16384)
    bbox: NormalizedBox
    confidence: float | None = Field(default=None, ge=0, le=1)
    tokens: tuple[TokenResult, ...] = Field(default=(), max_length=MAX_TOKENS)

    @model_validator(mode="after")
    def valid_children(self) -> Self:
        _unique([token.id for token in self.tokens], "token_id")
        _unique([str(token.reading_order) for token in self.tokens], "token_order")
        if any(token.line_id != self.id for token in self.tokens):
            raise ValueError("token_parent_mismatch")
        return self


class RegionResult(Boundary):
    id: StrictStr
    page_id: StrictStr
    reading_order: int = Field(ge=0)
    type: StrictStr
    bbox: NormalizedBox
    confidence: float | None = Field(default=None, ge=0, le=1)
    lines: tuple[LineResult, ...] = Field(default=(), max_length=MAX_LINES)

    @model_validator(mode="after")
    def valid_children(self) -> Self:
        _unique([line.id for line in self.lines], "line_id")
        _unique([str(line.reading_order) for line in self.lines], "line_order")
        if any(line.region_id != self.id for line in self.lines):
            raise ValueError("line_parent_mismatch")
        return self


class PageResult(Boundary):
    id: StrictStr
    document_id: StrictStr
    page_number: int = Field(gt=0)
    width_px: int = Field(gt=0)
    height_px: int = Field(gt=0)
    confidence: float | None = Field(default=None, ge=0, le=1)
    regions: tuple[RegionResult, ...] = Field(default=(), max_length=MAX_REGIONS)

    @model_validator(mode="after")
    def valid_children(self) -> Self:
        _unique([region.id for region in self.regions], "region_id")
        _unique([str(region.reading_order) for region in self.regions], "region_order")
        if any(region.page_id != self.id for region in self.regions):
            raise ValueError("region_parent_mismatch")
        return self


class ProvenanceResult(Boundary):
    input_sha256: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    configuration_sha256: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    engine_name: StrictStr = Field(min_length=1)
    engine_version: StrictStr = Field(min_length=1)
    model_version: StrictStr = Field(min_length=1)
    pipeline_version: StrictStr = Field(min_length=1)
    created_at: datetime
    attempt: int = Field(gt=0)

    @field_validator("created_at")
    @classmethod
    def utc_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(None):
            raise ValueError("provenance_timestamp_not_utc")
        return value


class WarningResult(Boundary):
    code: StrictStr = Field(max_length=128)
    message: StrictStr = Field(max_length=2048)


class RecognitionResult(Boundary):
    schema_version: str = Field(default="recognition-result/v1", pattern=r"^recognition-result/v1$")
    document_id: StrictStr
    raw_result_id: StrictStr
    current_revision_id: StrictStr
    provenance: ProvenanceResult
    pages: tuple[PageResult, ...] = Field(min_length=1, max_length=MAX_PAGES)
    plain_text: StrictStr = Field(max_length=MAX_RESULT_TEXT_CHARS)
    confidence: float | None = Field(default=None, ge=0, le=1)
    warnings: tuple[WarningResult, ...] = Field(default=(), max_length=128)

    @model_validator(mode="after")
    def valid_hierarchy(self) -> Self:
        if self.raw_result_id == self.current_revision_id:
            raise ValueError("raw_and_revision_ids_must_differ")
        _unique([page.id for page in self.pages], "page_id")
        _unique([str(page.page_number) for page in self.pages], "page_number")
        if any(page.document_id != self.document_id for page in self.pages):
            raise ValueError("page_parent_mismatch")
        all_ids = [self.document_id, self.raw_result_id, self.current_revision_id]
        region_count = line_count = token_count = 0
        text_chars = len(self.plain_text)
        for page in self.pages:
            all_ids.append(page.id)
            region_count += len(page.regions)
            for region in page.regions:
                all_ids.append(region.id)
                line_count += len(region.lines)
                for line in region.lines:
                    all_ids.append(line.id)
                    text_chars += len(line.text)
                    token_count += len(line.tokens)
                    for token in line.tokens:
                        all_ids.append(token.id)
                        text_chars += len(token.text)
                        text_chars += sum(len(alt.text) for alt in token.alternatives)
        if (
            region_count > MAX_TOTAL_REGIONS
            or line_count > MAX_TOTAL_LINES
            or token_count > MAX_TOTAL_TOKENS
            or text_chars > MAX_RESULT_TEXT_CHARS
        ):
            raise ValueError("result_aggregate_limit")
        _unique(all_ids, "hierarchy_id")
        for value in all_ids:
            _check_id(value)
        return self


class BoundaryValidationError(ValueError):
    """Safe machine-readable error without user text, paths, or Pydantic input values."""

    def __init__(self, codes: tuple[str, ...]):
        self.codes = codes
        super().__init__(",".join(codes))


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BoundaryValidationError(("duplicate_json_key",))
        result[key] = value
    return result


def _parse_json[B: Boundary](data: bytes, model: type[B], max_bytes: int) -> B:
    if not isinstance(data, bytes) or len(data) > max_bytes:
        raise BoundaryValidationError(("body_too_large_or_wrong_type",))
    try:
        json.loads(data.decode("utf-8"), object_pairs_hook=_unique_json_object)
    except BoundaryValidationError:
        raise
    except (ValueError, RecursionError):
        raise BoundaryValidationError(("json_invalid",)) from None
    try:
        return model.model_validate_json(data)
    except ValidationError as exc:
        codes = tuple(
            str(error["type"])[:64]
            for error in exc.errors(include_input=False, include_context=False)[:16]
        )
        raise BoundaryValidationError(codes or ("invalid_input",)) from None


def parse_request_json(data: bytes) -> RecognitionRequest:
    """Validate bounded request bytes without leaking their content on failure."""
    return _parse_json(data, RecognitionRequest, MAX_REQUEST_JSON_BYTES)


def parse_result_json(data: bytes) -> RecognitionResult:
    """Validate bounded result bytes before any persistence or serialization."""
    return _parse_json(data, RecognitionResult, MAX_RESULT_JSON_BYTES)
