"""Pure, bounded engine routing plans; no engine or binary input is executed here."""

from __future__ import annotations

from dataclasses import dataclass

from text_recognition_core.domain.values import PrivacyMode, RecognitionMode, StableId

_REGION_MODES = frozenset((RecognitionMode.OCR, RecognitionMode.HTR))


@dataclass(frozen=True, slots=True)
class EngineDescriptor:
    name: StableId
    version: str
    modes: frozenset[RecognitionMode]
    local: bool
    rank: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.name, StableId):
            raise ValueError("invalid_engine_name")
        if not isinstance(self.version, str) or not 0 < len(self.version) <= 64:
            raise ValueError("invalid_engine_version")
        if (
            not isinstance(self.modes, frozenset)
            or not self.modes
            or not self.modes <= _REGION_MODES
        ):
            raise ValueError("invalid_engine_capabilities")
        if type(self.local) is not bool:
            raise ValueError("invalid_engine_locality")
        if type(self.rank) is not int or not 0 <= self.rank <= 1000:
            raise ValueError("invalid_engine_rank")


@dataclass(frozen=True, slots=True)
class RegionRoute:
    region_id: StableId
    candidates: tuple[EngineDescriptor, ...]


@dataclass(frozen=True, slots=True)
class EngineRegistry:
    descriptors: tuple[EngineDescriptor, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.descriptors, tuple) or len(self.descriptors) > 32:
            raise ValueError("invalid_engine_registry")
        if any(not isinstance(descriptor, EngineDescriptor) for descriptor in self.descriptors):
            raise ValueError("invalid_engine_registry")
        if len({descriptor.name for descriptor in self.descriptors}) != len(self.descriptors):
            raise ValueError("duplicate_engine_name")

    def plan(
        self,
        mode: RecognitionMode,
        privacy: PrivacyMode,
        *,
        preferred: StableId | None = None,
    ) -> tuple[EngineDescriptor, ...]:
        if not isinstance(mode, RecognitionMode) or mode not in _REGION_MODES:
            raise ValueError("region_capability_required")
        if not isinstance(privacy, PrivacyMode):
            raise ValueError("invalid_privacy_mode")
        if preferred is not None:
            if not isinstance(preferred, StableId):
                raise ValueError("invalid_engine_name")
            chosen = next((item for item in self.descriptors if item.name == preferred), None)
            if chosen is None:
                raise ValueError("engine_unavailable")
            if mode not in chosen.modes:
                raise ValueError("engine_capability_unsupported")
            if privacy is PrivacyMode.LOCAL_ONLY and not chosen.local:
                raise ValueError("engine_privacy_denied")
            return (chosen,)
        candidates = tuple(
            sorted(
                (
                    item
                    for item in self.descriptors
                    if mode in item.modes and (privacy is not PrivacyMode.LOCAL_ONLY or item.local)
                ),
                key=lambda item: (item.rank, item.name.value),
            )
        )
        if not candidates:
            raise ValueError("engine_capability_unsupported")
        return candidates

    def plan_regions(
        self,
        regions: tuple[tuple[StableId, RecognitionMode], ...],
        privacy: PrivacyMode,
    ) -> tuple[RegionRoute, ...]:
        if not isinstance(regions, tuple) or len(regions) > 4096:
            raise ValueError("invalid_region_routes")
        if any(not isinstance(region, tuple) or len(region) != 2 for region in regions):
            raise ValueError("invalid_region_routes")
        ids = tuple(region_id for region_id, _ in regions)
        if any(not isinstance(region_id, StableId) for region_id in ids) or len(set(ids)) != len(
            ids
        ):
            raise ValueError("invalid_region_routes")
        return tuple(
            RegionRoute(region_id, self.plan(mode, privacy)) for region_id, mode in regions
        )
