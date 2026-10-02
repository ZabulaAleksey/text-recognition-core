from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import pytest
from test_docker_raster_contract import CID, IMAGE, NONCE, PIXELS, SOURCE, Scenario

from text_recognition_core.intake import docker_raster as raster
from text_recognition_core.intake.owned_decoder_cli import DecoderHelperError


@pytest.mark.parametrize("failure", ["empty-unacknowledged-create", "cleanup"])
def test_uncertain_cleanup_retains_immutable_identity_and_blocks_later_admission_without_cli(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    scenario = Scenario(monkeypatch, "cleanup" if failure == "cleanup" else "")
    original = scenario.call
    if failure == "empty-unacknowledged-create":

        def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
            if arguments[0] == "create":
                scenario.created = True
                scenario.calls.append(("create", {**kwargs, "arguments": arguments}))
                raise DecoderHelperError
            if arguments[0] == "ps":
                scenario.calls.append(("ps", {**kwargs, "arguments": arguments}))
                return 0, b"", b"", 0
            return original(arguments, **kwargs)

        monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$") as initial:
        scenario.decoder.decode(SOURCE, scenario.token)
    retained = scenario.decoder.pending_recovery
    assert retained is initial.value.recovery
    assert retained == raster.OwnedRasterRecovery(
        IMAGE,
        NONCE,
        CID if failure == "cleanup" else None,
    )
    assert retained is not None
    with pytest.raises(FrozenInstanceError):
        retained.nonce = "replacement"  # type: ignore[misc]
    before_retry = len(scenario.calls)
    for _ in range(2):
        with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$") as retry:
            scenario.decoder.decode(SOURCE + b"-different-valid-envelope", scenario.token)
        assert retry.value.recovery is retained
        assert scenario.decoder.pending_recovery is retained
        assert len(scenario.calls) == before_retry
    assert not scenario.decoder._lock.locked()


def test_unacknowledged_create_with_exact_discovered_cleanup_does_not_poison_instance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario = Scenario(monkeypatch)
    original = scenario.call
    interrupted = False

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        nonlocal interrupted
        if arguments[0] == "create":
            scenario.removed = scenario.started = False
            if not interrupted:
                interrupted = True
                scenario.created = True
                scenario.calls.append(("create", {**kwargs, "arguments": arguments}))
                raise DecoderHelperError
        return original(arguments, **kwargs)

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$") as initial:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert initial.value.recovery is None
    assert scenario.removed and scenario.decoder.pending_recovery is None
    result = scenario.decoder.decode(SOURCE, scenario.token)
    assert result.pixels == PIXELS
    assert scenario.removed and scenario.decoder.pending_recovery is None
    assert sum(name == "rm" for name, _ in scenario.calls) == 2


def test_successful_instance_reuses_admission_after_verified_cleanup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario = Scenario(monkeypatch)
    original = scenario.call

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        if arguments[0] == "create":
            scenario.removed = scenario.started = False
        return original(arguments, **kwargs)

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    first = scenario.decoder.decode(SOURCE, scenario.token)
    assert scenario.removed and scenario.decoder.pending_recovery is None
    second = scenario.decoder.decode(SOURCE, scenario.token)
    assert first == second
    assert scenario.removed and scenario.decoder.pending_recovery is None
    assert sum(name == "create" for name, _ in scenario.calls) == 2
    assert sum(name == "rm" for name, _ in scenario.calls) == 2
    assert not scenario.decoder._lock.locked()
