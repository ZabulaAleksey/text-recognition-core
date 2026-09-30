"""Immutable, framework-free values for the recognition domain."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from math import isfinite

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256 = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True, slots=True)
class StableId:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not _ID.fullmatch(self.value):
            raise ValueError("invalid_stable_id")


@dataclass(frozen=True, slots=True)
class Confidence:
    value: float

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise ValueError("invalid_confidence")
        if not isfinite(self.value) or not 0 <= self.value <= 1:
            raise ValueError("invalid_confidence")


@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def __post_init__(self) -> None:
        if any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not isfinite(v)
            or not 0 <= v <= 1
            for v in (self.x, self.y)
        ):
            raise ValueError("invalid_normalized_point")


@dataclass(frozen=True, slots=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        values = (self.x, self.y, self.width, self.height)
        if any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not isfinite(v)
            or not 0 <= v <= 1
            for v in values
        ):
            raise ValueError("invalid_normalized_bbox")
        if (
            self.width <= 0
            or self.height <= 0
            or self.x + self.width > 1
            or self.y + self.height > 1
        ):
            raise ValueError("bbox_outside_page")


class RecognitionMode(StrEnum):
    AUTO = "AUTO"
    OCR = "OCR"
    HTR = "HTR"
    MIXED = "MIXED"


class BatchPolicy(StrEnum):
    ALL_OR_NOTHING = "ALL_OR_NOTHING"
    ALLOW_PARTIAL = "ALLOW_PARTIAL"


class PrivacyMode(StrEnum):
    LOCAL_ONLY = "LOCAL_ONLY"
    HYBRID = "HYBRID"
    REMOTE_ALLOWED = "REMOTE_ALLOWED"


class ErrorCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    CAPABILITY_UNSUPPORTED = "CAPABILITY_UNSUPPORTED"
    ENGINE_FAILED = "ENGINE_FAILED"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, slots=True)
class Provenance:
    input_sha256: str
    configuration_sha256: str
    engine_name: str
    engine_version: str
    model_version: str
    pipeline_version: str
    created_at: datetime
    attempt: int

    def __post_init__(self) -> None:
        if not _SHA256.fullmatch(self.input_sha256) or not _SHA256.fullmatch(
            self.configuration_sha256
        ):
            raise ValueError("invalid_provenance_hash")
        if not all(
            (self.engine_name, self.engine_version, self.model_version, self.pipeline_version)
        ):
            raise ValueError("missing_provenance_version")
        if (
            not isinstance(self.created_at, datetime)
            or self.created_at.tzinfo is None
            or self.created_at.utcoffset() != UTC.utcoffset(None)
        ):
            raise ValueError("provenance_timestamp_not_utc")
        if type(self.attempt) is not int or self.attempt < 1:
            raise ValueError("invalid_provenance_attempt")
