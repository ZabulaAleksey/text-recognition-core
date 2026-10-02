from __future__ import annotations

import asyncio
import io
import os
import sys
from dataclasses import FrozenInstanceError
from typing import Any

import pytest
from test_docker_raster_contract import CID, IMAGE, NONCE, SOURCE, Scenario

from text_recognition_core.intake import docker_raster as raster
from text_recognition_core.intake import owned_decoder_cli as cli


@pytest.mark.parametrize("phase", ["rm", "final-ps"])
@pytest.mark.parametrize("interruption_type", [KeyboardInterrupt, asyncio.CancelledError])
def test_cleanup_interruption_preserves_original_and_blocks_later_admission(
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
    interruption_type: type[BaseException],
) -> None:
    scenario = Scenario(monkeypatch)
    original = scenario.call
    interruption = interruption_type()

    def call(arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        interrupted = (
            arguments[0] == "rm" if phase == "rm" else (arguments[0] == "ps" and scenario.removed)
        )
        if interrupted:
            assert kwargs["cancelled"]() is False
            assert kwargs["deadline"] == kwargs["cleanup_deadline"] == 120.0
            scenario.calls.append((arguments[0], {**kwargs, "arguments": arguments}))
            raise interruption
        return original(arguments, **kwargs)

    monkeypatch.setattr(scenario.decoder, "_cli", call)
    with pytest.raises(interruption_type) as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert raised.value is interruption
    retained = scenario.decoder.pending_recovery
    assert retained == raster.OwnedRasterRecovery(IMAGE, NONCE, CID)
    assert retained is not None
    with pytest.raises(FrozenInstanceError):
        retained.container_id = None  # type: ignore[misc]
    before_retry = len(scenario.calls)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$") as retry:
        scenario.decoder.decode(SOURCE + b"-next", scenario.token)
    assert retry.value.recovery is retained
    assert len(scenario.calls) == before_retry
    assert not scenario.decoder._lock.locked()
    assert scenario.removed == (phase == "final-ps")


@pytest.mark.skipif(os.name != "nt", reason="Windows-only owned helper admission")
@pytest.mark.parametrize("fault", ["job", "kill", "pipe", "job-then-pipe", "alive"])
@pytest.mark.parametrize("interruption_type", [KeyboardInterrupt, asyncio.CancelledError])
def test_helper_cleanup_interruption_still_attempts_remaining_bounded_resources(
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
    interruption_type: type[BaseException],
) -> None:
    interruption = interruption_type()
    later_interruption = asyncio.CancelledError()
    calls: list[str] = []

    class Pipe(io.BytesIO):
        def __init__(self, name: str) -> None:
            super().__init__()
            self.name = name

        def close(self) -> None:
            calls.append("close-" + self.name)
            super().close()
            if self.name == "stdin" and fault == "pipe":
                raise interruption
            if self.name == "stdin" and fault == "job-then-pipe":
                raise later_interruption

    class Process:
        stdin, stdout, stderr = Pipe("stdin"), Pipe("stdout"), Pipe("stderr")

        def poll(self) -> None:
            return None

        def kill(self) -> None:
            calls.append("kill")
            if fault == "kill":
                raise interruption

        def wait(self, timeout: float) -> int:
            assert 0 <= timeout <= 1
            calls.append("wait")
            return 0

    class Job:
        def assign_and_resume(self, process: Any) -> None:
            calls.append("assign")

        def close(self, deadline: float) -> None:
            calls.append("job-close")
            assert deadline == 103.0
            if fault in ("job", "job-then-pipe"):
                raise interruption

    threads: list[Any] = []

    class Thread:
        def __init__(self, **kwargs: Any) -> None:
            self.index = len(threads)
            threads.append(self)

        def start(self) -> None:
            calls.append(f"start-{self.index}")

        def join(self, timeout: float) -> None:
            assert 0 <= timeout <= 1
            calls.append(f"join-{self.index}")

        def is_alive(self) -> bool:
            calls.append(f"alive-{self.index}")
            if fault == "alive" and self.index == 0:
                raise interruption
            return False

    process = Process()
    monkeypatch.setattr(cli, "_WindowsJob", Job)
    monkeypatch.setattr(cli.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(cli.threading, "Thread", Thread)
    monkeypatch.setattr(cli.time, "monotonic", lambda: 100.0)
    checks = 0

    def cancelled() -> bool:
        nonlocal checks
        checks += 1
        return checks > 1

    with pytest.raises(interruption_type) as raised:
        cli.run_owned_cli(
            [sys._base_executable, "-I", "-B", "-c", ""],
            env={},
            source=b"public",
            deadline=102.0,
            cleanup_deadline=103.0,
            cancelled=cancelled,
        )
    assert raised.value is interruption
    assert "assign" in calls and "job-close" in calls and "kill" in calls and "wait" in calls
    assert all(f"join-{index}" in calls for index in range(3))
    assert all("close-" + name in calls for name in ("stdin", "stdout", "stderr"))
    assert all(pipe.closed for pipe in (process.stdin, process.stdout, process.stderr))
    assert calls.index("wait") < calls.index("join-0") < calls.index("close-stdin")

    if fault == "alive":
        assert all(f"alive-{index}" in calls for index in range(3))
        assert calls.index("alive-0") < calls.index("close-stdin")
