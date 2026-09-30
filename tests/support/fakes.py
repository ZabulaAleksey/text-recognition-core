"""Port doubles with deterministic identity, time, cancellation and raw storage."""

from __future__ import annotations

from datetime import UTC, datetime

from text_recognition_core.domain.model import Document
from text_recognition_core.domain.values import StableId


class SequenceIds:
    def __init__(self) -> None:
        self.next_value = 0

    def new_id(self) -> StableId:
        self.next_value += 1
        return StableId(f"test-{self.next_value}")


class FixedClock:
    def __init__(self, instant: datetime) -> None:
        if instant.tzinfo is None or instant.utcoffset() != UTC.utcoffset(None):
            raise ValueError("clock_requires_utc")
        self.instant = instant

    def now_utc(self) -> datetime:
        return self.instant


class FlagCancellation:
    def __init__(self) -> None:
        self.requested = False

    def cancelled(self) -> bool:
        return self.requested


class MemoryDocumentStore:
    def __init__(self) -> None:
        self.documents: dict[StableId, Document] = {}

    def append_raw(self, document: Document) -> None:
        if document.id in self.documents:
            raise ValueError("raw_document_already_exists")
        self.documents[document.id] = document

    def get(self, document_id: StableId) -> Document | None:
        return self.documents.get(document_id)
