"""Immutable raw hierarchy; current revisions are identified separately."""

from __future__ import annotations

from dataclasses import dataclass

from .values import BoundingBox, Confidence, Point, PrivacyMode, Provenance, StableId


def _unique(ids: tuple[StableId, ...], label: str) -> None:
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate_{label}_id")


def _ordered(orders: tuple[int, ...], label: str) -> None:
    if any(type(order) is not int or order < 0 for order in orders) or len(orders) != len(
        set(orders)
    ):
        raise ValueError(f"invalid_{label}_reading_order")


@dataclass(frozen=True, slots=True)
class Alternative:
    text: str
    confidence: Confidence


@dataclass(frozen=True, slots=True)
class Token:
    id: StableId
    line_id: StableId
    reading_order: int
    text: str
    bbox: BoundingBox
    confidence: Confidence | None = None
    alternatives: tuple[Alternative, ...] = ()

    def __post_init__(self) -> None:
        _ordered((self.reading_order,), "token")
        if not isinstance(self.alternatives, tuple):
            raise ValueError("mutable_alternatives")


@dataclass(frozen=True, slots=True)
class Line:
    id: StableId
    region_id: StableId
    reading_order: int
    bbox: BoundingBox
    text: str
    tokens: tuple[Token, ...] = ()
    confidence: Confidence | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.tokens, tuple):
            raise ValueError("mutable_tokens")
        _ordered((self.reading_order,), "line")
        _unique(tuple(token.id for token in self.tokens), "token")
        _ordered(tuple(token.reading_order for token in self.tokens), "token")
        if any(token.line_id != self.id for token in self.tokens):
            raise ValueError("token_parent_mismatch")


@dataclass(frozen=True, slots=True)
class Region:
    id: StableId
    page_id: StableId
    reading_order: int
    type: str
    bbox: BoundingBox
    lines: tuple[Line, ...] = ()
    polygon: tuple[Point, ...] = ()
    confidence: Confidence | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.lines, tuple) or not isinstance(self.polygon, tuple):
            raise ValueError("mutable_region_children")
        _ordered((self.reading_order,), "region")
        _unique(tuple(line.id for line in self.lines), "line")
        _ordered(tuple(line.reading_order for line in self.lines), "line")
        if any(line.region_id != self.id for line in self.lines):
            raise ValueError("line_parent_mismatch")
        if self.polygon and (
            len(self.polygon) < 3
            or any(
                point.x < self.bbox.x
                or point.x > self.bbox.x + self.bbox.width
                or point.y < self.bbox.y
                or point.y > self.bbox.y + self.bbox.height
                for point in self.polygon
            )
        ):
            raise ValueError("polygon_outside_bbox")


@dataclass(frozen=True, slots=True)
class Page:
    id: StableId
    document_id: StableId
    page_number: int
    width_px: int
    height_px: int
    regions: tuple[Region, ...] = ()
    confidence: Confidence | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.regions, tuple):
            raise ValueError("mutable_regions")
        if any(
            type(v) is not int or v <= 0 for v in (self.page_number, self.width_px, self.height_px)
        ):
            raise ValueError("invalid_page_dimensions")
        _unique(tuple(region.id for region in self.regions), "region")
        _ordered(tuple(region.reading_order for region in self.regions), "region")
        if any(region.page_id != self.id for region in self.regions):
            raise ValueError("region_parent_mismatch")


@dataclass(frozen=True, slots=True)
class Document:
    id: StableId
    source_id: StableId
    raw_result_id: StableId
    current_revision_id: StableId
    privacy_mode: PrivacyMode
    pages: tuple[Page, ...]
    provenance: Provenance
    schema_version: str = "recognition-result/v1"

    def __post_init__(self) -> None:
        if not isinstance(self.pages, tuple) or not self.pages:
            raise ValueError("document_pages_required")
        if self.raw_result_id == self.current_revision_id:
            raise ValueError("raw_and_revision_ids_must_differ")
        _unique(tuple(page.id for page in self.pages), "page")
        numbers = tuple(page.page_number for page in self.pages)
        if len(numbers) != len(set(numbers)):
            raise ValueError("duplicate_page_number")
        if any(page.document_id != self.id for page in self.pages):
            raise ValueError("page_parent_mismatch")
        all_ids = [self.id, self.source_id, self.raw_result_id, self.current_revision_id]
        for page in self.pages:
            all_ids.append(page.id)
            for region in page.regions:
                all_ids.append(region.id)
                for line in region.lines:
                    all_ids.append(line.id)
                    all_ids.extend(token.id for token in line.tokens)
        _unique(tuple(all_ids), "hierarchy")
