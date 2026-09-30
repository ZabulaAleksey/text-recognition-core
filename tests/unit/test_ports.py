from datetime import UTC, datetime

import pytest

from tests.support.fakes import FixedClock, FlagCancellation, MemoryDocumentStore, SequenceIds
from text_recognition_core.application.ports import (
    CancellationToken,
    Clock,
    DocumentStore,
    IdFactory,
)
from text_recognition_core.domain.model import Document, Page
from text_recognition_core.domain.values import PrivacyMode, Provenance, StableId


def test_deterministic_port_doubles_and_append_only_raw() -> None:
    ids: IdFactory = SequenceIds()
    clock: Clock = FixedClock(datetime(2026, 9, 30, tzinfo=UTC))
    cancel: CancellationToken = FlagCancellation()
    store: DocumentStore = MemoryDocumentStore()
    document_id, source_id, raw_id, revision_id, page_id = (ids.new_id() for _ in range(5))
    document = Document(
        document_id,
        source_id,
        raw_id,
        revision_id,
        PrivacyMode.LOCAL_ONLY,
        (Page(page_id, document_id, 1, 100, 100),),
        Provenance("a" * 64, "b" * 64, "fake", "1", "none", "1", clock.now_utc(), 1),
    )
    assert not cancel.cancelled()
    store.append_raw(document)
    assert store.get(document_id) is document
    assert store.get(StableId("unknown")) is None
    with pytest.raises(ValueError, match="raw_document_already_exists"):
        store.append_raw(document)
