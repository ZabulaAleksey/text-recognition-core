"""Ports only; no concrete engine, storage, worker, or transport adapter."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from text_recognition_core.domain.model import Document
from text_recognition_core.domain.values import StableId


class IdFactory(Protocol):
    def new_id(self) -> StableId: ...


class Clock(Protocol):
    def now_utc(self) -> datetime: ...


class CancellationToken(Protocol):
    def cancelled(self) -> bool: ...


class RecognitionEngine(Protocol):
    def capabilities(self) -> frozenset[str]: ...

    def version(self) -> str: ...

    def recognize(self, source_id: StableId, cancellation: CancellationToken) -> Document: ...


class DocumentStore(Protocol):
    def append_raw(self, document: Document) -> None: ...

    def get(self, document_id: StableId) -> Document | None: ...


class JobScheduler(Protocol):
    def enqueue(self, source_id: StableId) -> StableId: ...
