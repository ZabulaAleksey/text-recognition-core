from __future__ import annotations

import subprocess
import sys
from typing import Any

import pytest

from tools import printed_golden_smoke


def _record_processes(monkeypatch: pytest.MonkeyPatch) -> list[subprocess.Popen[bytes]]:
    spawned: list[subprocess.Popen[bytes]] = []
    real_popen = subprocess.Popen

    def recording_popen(*args: Any, **kwargs: Any) -> subprocess.Popen[bytes]:
        process = real_popen(*args, **kwargs)
        spawned.append(process)
        return process

    monkeypatch.setattr(printed_golden_smoke.subprocess, "Popen", recording_popen)
    return spawned


def test_joint_output_cap_stops_real_child_flooding_both_streams(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spawned = _record_processes(monkeypatch)
    code = (
        "import os, threading; "
        "f=lambda fd, byte: [os.write(fd, byte*4096) for _ in range(128)]; "
        "a=threading.Thread(target=f,args=(1,b'x')); "
        "b=threading.Thread(target=f,args=(2,b'y')); "
        "a.start(); b.start(); a.join(); b.join()"
    )

    with pytest.raises(printed_golden_smoke.CandidateProcessError, match="exceeded"):
        printed_golden_smoke._run_bounded_process(
            [sys.executable, "-c", code], timeout_seconds=2, max_output_bytes=1024
        )

    assert len(spawned) == 1
    assert spawned[0].poll() is not None
    assert spawned[0].returncode is not None


def test_joint_output_limit_accepts_exact_boundary_and_decodes_utf8() -> None:
    code = "import os; os.write(1, b'abc\\xd0\\x90'); os.write(2, b'12345')"
    stdout, stderr, returncode = printed_golden_smoke._run_bounded_process(
        [sys.executable, "-c", code], timeout_seconds=2, max_output_bytes=12
    )

    assert returncode == 0
    assert stdout == "abcА"
    assert stderr == "12345"


def test_stdout_and_stderr_share_one_joint_budget() -> None:
    code = "import os; os.write(1, b'x'*700); os.write(2, b'y'*700)"

    with pytest.raises(printed_golden_smoke.CandidateProcessError, match="exceeded"):
        printed_golden_smoke._run_bounded_process(
            [sys.executable, "-c", code], timeout_seconds=2, max_output_bytes=1024
        )


def test_invalid_utf8_output_fails_without_replacement() -> None:
    code = "import os; os.write(1, b'valid\\xfftext')"

    with pytest.raises(printed_golden_smoke.CandidateProcessError, match="not valid UTF-8"):
        printed_golden_smoke._run_bounded_process([sys.executable, "-c", code], timeout_seconds=2)


def test_process_start_error_does_not_expose_command_or_start_a_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = "private-executable-path-sentinel"
    attempted_commands: list[list[str]] = []

    def fail_to_start(args: Any, *_args: Any, **_kwargs: Any) -> subprocess.Popen[bytes]:
        attempted_commands.append(list(args))
        raise OSError(sentinel)

    monkeypatch.setattr(printed_golden_smoke.subprocess, "Popen", fail_to_start)
    with pytest.raises(
        printed_golden_smoke.CandidateProcessError, match="process start failed"
    ) as error:
        printed_golden_smoke._run_bounded_process([sentinel, "--version"], timeout_seconds=2)

    assert sentinel not in str(error.value)
    assert attempted_commands == [[sentinel, "--version"]]


def test_timeout_kills_and_reaps_the_exact_direct_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spawned = _record_processes(monkeypatch)

    with pytest.raises(printed_golden_smoke.CandidateProcessError, match="timed out"):
        printed_golden_smoke._run_bounded_process(
            [sys.executable, "-c", "import time; time.sleep(10)"], timeout_seconds=0.5
        )

    assert len(spawned) == 1
    assert spawned[0].poll() is not None
    assert spawned[0].returncode is not None


def test_output_read_failure_kills_and_reaps_the_exact_direct_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spawned: list[subprocess.Popen[bytes]] = []
    real_popen = subprocess.Popen

    class BrokenReader:
        def __init__(self, stream: Any) -> None:
            self._stream = stream

        def read(self, _size: int) -> bytes:
            raise OSError("fixture read failure")

        def close(self) -> None:
            self._stream.close()

    class ProcessProxy:
        def __init__(self, process: subprocess.Popen[bytes]) -> None:
            self._process = process
            self.stdout = BrokenReader(process.stdout)
            self.stderr = process.stderr

        def __getattr__(self, name: str) -> Any:
            return getattr(self._process, name)

    def broken_stdout_popen(*args: Any, **kwargs: Any) -> ProcessProxy:
        process = real_popen(*args, **kwargs)
        spawned.append(process)
        return ProcessProxy(process)

    monkeypatch.setattr(printed_golden_smoke.subprocess, "Popen", broken_stdout_popen)

    with pytest.raises(printed_golden_smoke.CandidateProcessError, match="read failed"):
        printed_golden_smoke._run_bounded_process(
            [sys.executable, "-c", "import time; time.sleep(10)"], timeout_seconds=2
        )

    assert len(spawned) == 1
    assert spawned[0].poll() is not None
    assert spawned[0].returncode is not None
