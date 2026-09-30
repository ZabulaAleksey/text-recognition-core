from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from text_recognition_core.domain.model import Document, Line, Page, Region, Token
from text_recognition_core.domain.values import (
    BoundingBox,
    Confidence,
    Point,
    PrivacyMode,
    Provenance,
    StableId,
)


def ident(name: str) -> StableId:
    return StableId(name)


def sample() -> Document:
    box = BoundingBox(0.1, 0.1, 0.2, 0.2)
    token = Token(ident("token-1"), ident("line-1"), 0, "hello", box)
    line = Line(ident("line-1"), ident("region-1"), 0, box, "hello", (token,))
    region = Region(ident("region-1"), ident("page-1"), 0, "paragraph", box, (line,))
    page = Page(ident("page-1"), ident("doc-1"), 1, 100, 200, (region,))
    provenance = Provenance("a" * 64, "b" * 64, "fake", "1", "none", "1", datetime.now(UTC), 1)
    return Document(
        ident("doc-1"),
        ident("source-1"),
        ident("raw-1"),
        ident("revision-1"),
        PrivacyMode.LOCAL_ONLY,
        (page,),
        provenance,
    )


def test_immutable_hierarchy_preserves_raw_revision_separation() -> None:
    document = sample()
    assert document.raw_result_id != document.current_revision_id
    assert document.pages[0].regions[0].lines[0].tokens[0].text == "hello"
    with pytest.raises(FrozenInstanceError):
        document.pages = ()  # type: ignore[misc]
    with pytest.raises(ValueError, match="mutable_regions"):
        Page(ident("page-2"), ident("doc-1"), 2, 10, 10, [])  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 1.1, True])
def test_confidence_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError, match="invalid_confidence"):
        Confidence(value)


@pytest.mark.parametrize(
    "values",
    [(0.9, 0.1, 0.2, 0.2), (0.1, 0.1, -0.1, 0.2), (float("nan"), 0, 0.2, 0.2), (0, 0, 0, 1)],
)
def test_bbox_rejects_out_of_page_and_degenerate(values: tuple[float, ...]) -> None:
    with pytest.raises(ValueError):
        BoundingBox(*values)


def test_parent_and_order_checks_fail_closed() -> None:
    box = BoundingBox(0.1, 0.1, 0.2, 0.2)
    foreign = Token(ident("token-1"), ident("other-line"), 0, "x", box)
    with pytest.raises(ValueError, match="token_parent_mismatch"):
        Line(ident("line-1"), ident("region-1"), 0, box, "x", (foreign,))
    with pytest.raises(ValueError, match="duplicate_token_id"):
        same = Token(ident("token-1"), ident("line-1"), 0, "x", box)
        Line(ident("line-1"), ident("region-1"), 0, box, "x", (same, same))
    with pytest.raises(ValueError, match="polygon_outside_bbox"):
        Region(
            ident("region-1"),
            ident("page-1"),
            0,
            "text",
            box,
            polygon=(Point(0.1, 0.1), Point(0.2, 0.1), Point(0.9, 0.9)),
        )


def test_provenance_requires_utc_and_digests() -> None:
    with pytest.raises(ValueError, match="invalid_provenance_hash"):
        Provenance("BAD", "b" * 64, "engine", "1", "model", "pipeline", datetime.now(UTC), 1)
    with pytest.raises(ValueError, match="provenance_timestamp_not_utc"):
        Provenance(
            "a" * 64,
            "b" * 64,
            "engine",
            "1",
            "model",
            "pipeline",
            datetime.now().replace(tzinfo=None),
            1,
        )
