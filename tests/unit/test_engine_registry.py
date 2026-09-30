import pytest

from text_recognition_core.application.registry import EngineDescriptor, EngineRegistry
from text_recognition_core.domain.values import PrivacyMode, RecognitionMode, StableId


def descriptor(
    name: str,
    *modes: RecognitionMode,
    local: bool = True,
    rank: int = 0,
) -> EngineDescriptor:
    return EngineDescriptor(StableId(name), "1.0", frozenset(modes), local, rank)


def test_auto_plan_is_deterministic_and_exposes_ordered_fallback_only() -> None:
    registry = EngineRegistry(
        (
            descriptor("z", RecognitionMode.OCR, rank=2),
            descriptor("b", RecognitionMode.OCR),
            descriptor("a", RecognitionMode.OCR),
        )
    )
    assert tuple(
        item.name.value for item in registry.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY)
    ) == (
        "a",
        "b",
        "z",
    )


def test_explicit_engine_never_silently_falls_back() -> None:
    registry = EngineRegistry(
        (descriptor("ocr", RecognitionMode.OCR), descriptor("htr", RecognitionMode.HTR))
    )
    assert registry.plan(
        RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY, preferred=StableId("ocr")
    ) == (registry.descriptors[0],)
    with pytest.raises(ValueError, match="engine_unavailable"):
        registry.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY, preferred=StableId("unknown"))
    with pytest.raises(ValueError, match="engine_capability_unsupported"):
        registry.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY, preferred=StableId("htr"))


def test_local_only_excludes_remote_before_routing() -> None:
    remote = descriptor("remote", RecognitionMode.OCR, local=False)
    local = descriptor("local", RecognitionMode.OCR, rank=1)
    registry = EngineRegistry((remote, local))
    assert registry.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY) == (local,)
    with pytest.raises(ValueError, match="engine_privacy_denied"):
        registry.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY, preferred=remote.name)
    assert registry.plan(RecognitionMode.OCR, PrivacyMode.HYBRID) == (remote, local)


def test_unknown_region_capability_and_empty_eligible_set_fail_closed() -> None:
    registry = EngineRegistry((descriptor("ocr", RecognitionMode.OCR),))
    with pytest.raises(ValueError, match="region_capability_required"):
        registry.plan(RecognitionMode.AUTO, PrivacyMode.LOCAL_ONLY)
    with pytest.raises(ValueError, match="engine_capability_unsupported"):
        registry.plan(RecognitionMode.HTR, PrivacyMode.LOCAL_ONLY)
    with pytest.raises(ValueError, match="region_capability_required"):
        registry.plan([], PrivacyMode.LOCAL_ONLY)  # type: ignore[arg-type]
    remote_only = EngineRegistry((descriptor("remote", RecognitionMode.OCR, local=False),))
    with pytest.raises(ValueError, match="engine_capability_unsupported"):
        remote_only.plan(RecognitionMode.OCR, PrivacyMode.LOCAL_ONLY)


def test_registry_rejects_duplicate_or_malformed_descriptors() -> None:
    entry = descriptor("same", RecognitionMode.OCR)
    with pytest.raises(ValueError, match="duplicate_engine_name"):
        EngineRegistry((entry, entry))
    with pytest.raises(ValueError, match="invalid_engine_capabilities"):
        descriptor("invalid", RecognitionMode.AUTO)
    with pytest.raises(ValueError, match="invalid_engine_registry"):
        EngineRegistry((entry,) * 33)


def test_region_routing_preserves_order_and_rejects_missing_or_duplicate_regions() -> None:
    registry = EngineRegistry(
        (descriptor("ocr", RecognitionMode.OCR), descriptor("htr", RecognitionMode.HTR))
    )
    first, second = StableId("region-1"), StableId("region-2")
    routes = registry.plan_regions(
        ((first, RecognitionMode.OCR), (second, RecognitionMode.HTR)),
        PrivacyMode.LOCAL_ONLY,
    )
    assert [(route.region_id, route.candidates[0].name.value) for route in routes] == [
        (first, "ocr"),
        (second, "htr"),
    ]
    with pytest.raises(ValueError, match="invalid_region_routes"):
        registry.plan_regions(
            ((first, RecognitionMode.OCR), (first, RecognitionMode.HTR)), PrivacyMode.LOCAL_ONLY
        )
    with pytest.raises(ValueError, match="region_capability_required"):
        registry.plan_regions(
            ((first, RecognitionMode.OCR), (second, RecognitionMode.MIXED)), PrivacyMode.LOCAL_ONLY
        )
