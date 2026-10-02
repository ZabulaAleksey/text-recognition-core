from __future__ import annotations

import json
from typing import Any

import pytest
from test_docker_raster_contract import CID, IMAGE, NONCE, SOURCE, Scenario

from text_recognition_core.intake import docker_raster as raster
from text_recognition_core.intake.owned_decoder_cli import DecoderHelperError


@pytest.mark.parametrize("image_config", [None, "PUBLIC-CANARY", [], True, {}, {"Env": None}])
def test_malformed_image_config_fails_fixed_before_any_creation(
    monkeypatch: pytest.MonkeyPatch,
    image_config: Any,
) -> None:
    scenario = Scenario(monkeypatch)

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        scenario.calls.append((arguments[0], {**kwargs, "arguments": arguments}))
        assert arguments[0] == "image"
        raw = {"Id": IMAGE, "Os": "linux", "Architecture": "amd64", "Config": image_config}
        return 0, json.dumps(raw).encode(), b"", 0

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(raster.RasterDecoderError) as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert raised.value.code == "DECODER_UNAVAILABLE"
    assert str(raised.value) == "DECODER_UNAVAILABLE"
    assert raised.value.recovery is None
    assert [phase for phase, _ in scenario.calls] == ["image"]
    assert not scenario.created and not scenario.started and not scenario.removed


@pytest.mark.parametrize("phase", ["rm", "final-ps"])
def test_cancellation_during_cleanup_finishes_cleanup_and_withholds_valid_raster(
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    scenario = Scenario(monkeypatch)
    original = scenario.call

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        if arguments[0] == "rm" and phase == "rm":
            scenario.token.stopped = True
        if arguments[0] == "ps" and scenario.removed and phase == "final-ps":
            scenario.token.stopped = True
        return original(arguments, **kwargs)

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_CANCELLED$") as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert raised.value.recovery is None
    assert scenario.started and scenario.removed and scenario.token.stopped
    assert scenario.calls[-1][0] == "ps"
    assert sum(name == "rm" for name, _ in scenario.calls) == 1
    cleanup = [kwargs for _, kwargs in scenario.calls if kwargs["deadline"] == 120.0]
    assert cleanup and all(kwargs["cancelled"]() is False for kwargs in cleanup)
    assert all(kwargs["cleanup_deadline"] == 120.0 for _, kwargs in scenario.calls)


@pytest.mark.parametrize("discovered", [False, True])
def test_unacknowledged_create_requires_nonce_recovery_unless_exact_owned_cid_is_cleaned(
    monkeypatch: pytest.MonkeyPatch,
    discovered: bool,
) -> None:
    scenario = Scenario(monkeypatch)
    original = scenario.call

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        if arguments[0] == "create":
            scenario.created = True
            scenario.calls.append(("create", {**kwargs, "arguments": arguments}))
            # Parent helper exit is not evidence the submitted daemon request was cancelled.
            raise DecoderHelperError
        if arguments[0] == "ps" and not discovered:
            scenario.calls.append(("ps", {**kwargs, "arguments": arguments}))
            return 0, b"", b"", 0
        return original(arguments, **kwargs)

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$") as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert not scenario.started
    if discovered:
        assert scenario.removed
        assert raised.value.recovery is None
        removals = [kwargs["arguments"] for name, kwargs in scenario.calls if name == "rm"]
        assert removals == [["rm", "-f", CID]]
        assert scenario.calls[-1][0] == "ps"
    else:
        assert raised.value.recovery == raster.OwnedRasterRecovery(IMAGE, NONCE, None)
        assert not scenario.removed
        assert not any(name in ("rm", "inspect", "start") for name, _ in scenario.calls)
    assert all(kwargs["cancelled"]() is False for name, kwargs in scenario.calls if name == "ps")
