from __future__ import annotations

import ctypes
import io
import json
import os
import sys
import time
from ctypes import wintypes
from typing import Any

import pytest

from text_recognition_core.intake import owned_decoder_cli as cli

pytestmark = pytest.mark.skipif(os.name != "nt", reason="native Windows Job contracts")


def native_command(code: str) -> list[str]:
    return [sys._base_executable, "-I", "-B", "-c", code]


def native_env() -> dict[str, str]:
    return {
        key: os.environ[key] for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP") if key in os.environ
    }


def test_native_bidirectional_stream_bytecount_and_stdin_eof() -> None:
    source = bytes(range(256)) * 1024
    deadline = time.monotonic() + 4
    result = cli.run_owned_cli(
        native_command(
            "import sys;data=sys.stdin.buffer.read();"
            "sys.stdout.buffer.write(data[::-1]);"
            "sys.stderr.buffer.write(str(len(data)).encode())"
        ),
        env=native_env(),
        deadline=deadline,
        cleanup_deadline=deadline + 2,
        cancelled=lambda: False,
        source=source,
        stdout_limit=len(source),
        stderr_limit=16,
        combined_limit=len(source) + 16,
    )
    assert result == (0, source[::-1], b"262144", len(source))


def observe_job_accounting(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    counts: list[int] = []
    original = cli._WindowsJob

    class QueryProbe:
        def __init__(self, function: Any) -> None:
            object.__setattr__(self, "function", function)

        def __setattr__(self, name: str, value: Any) -> None:
            setattr(self.function, name, value)

        def __call__(self, *args: Any) -> Any:
            result = self.function(*args)
            if result:
                counts.append(args[2]._obj.active)
            return result

    class KernelProxy:
        def __init__(self, api: Any) -> None:
            self.api = api
            self.query = QueryProbe(api.QueryInformationJobObject)

        def __getattr__(self, name: str) -> Any:
            return self.query if name == "QueryInformationJobObject" else getattr(self.api, name)

    class ObservedJob(original):
        def __init__(self) -> None:
            super().__init__()
            self._kernel = KernelProxy(self._kernel)

    monkeypatch.setattr(cli, "_WindowsJob", ObservedJob)
    return counts


@pytest.mark.parametrize("stop", ["timeout", "cancel"])
def test_native_stop_reaps_observed_parent_and_descendant_job_to_zero(
    monkeypatch: pytest.MonkeyPatch, stop: str
) -> None:
    counts = observe_job_accounting(monkeypatch)
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    api.OpenProcess.restype = wintypes.HANDLE
    api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    api.WaitForSingleObject.restype = wintypes.DWORD
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    handles: list[Any] = []
    captured = bytearray()
    observed = False

    def capture(chunk: bytes) -> None:
        nonlocal observed
        captured.extend(chunk)
        if not observed and b"\n" in captured:
            pids = json.loads(captured)
            assert pids[0] != pids[1]
            for pid in pids:
                handle = api.OpenProcess(0x100000, False, pid)
                assert handle
                handles.append(handle)
            observed = True

    code = (
        "import os,subprocess,sys,time,json;"
        "child=subprocess.Popen([sys.executable,'-I','-B','-c',"
        "'import time;time.sleep(30)']);"
        "print(json.dumps([os.getpid(),child.pid]),flush=True);time.sleep(30)"
    )
    deadline = time.monotonic() + 1.5
    started = time.monotonic()
    try:
        with pytest.raises(cli.DecoderHelperError, match="^DECODER_UNAVAILABLE$"):
            cli.run_owned_cli(
                native_command(code),
                env=native_env(),
                deadline=deadline,
                cleanup_deadline=deadline + 2,
                cancelled=lambda: observed and stop == "cancel",
                on_stdout=capture,
            )
        assert observed and len(handles) == 2
        assert counts and counts[-1] == 0
        assert all(api.WaitForSingleObject(handle, 1000) == 0 for handle in handles)
        assert time.monotonic() - started < 4.5
    finally:
        for handle in handles:
            assert api.CloseHandle(handle)


@pytest.mark.parametrize("individual_cap", [True, False])
def test_concurrent_output_overflow_denies_without_echo(individual_cap: bool) -> None:
    code = (
        "import sys,threading;"
        "threads=[threading.Thread(target=lambda s=s:s.write(b'PUBLIC-CANARY'*4096))"
        " for s in (sys.stdout.buffer,sys.stderr.buffer)];"
        "[t.start() for t in threads];[t.join() for t in threads]"
    )
    deadline = time.monotonic() + 3
    with pytest.raises(cli.DecoderHelperError) as raised:
        cli.run_owned_cli(
            native_command(code),
            env=native_env(),
            deadline=deadline,
            cleanup_deadline=deadline + 2,
            cancelled=lambda: False,
            stdout_limit=128 if individual_cap else 65536,
            stderr_limit=128 if individual_cap else 65536,
            combined_limit=None if individual_cap else 65536,
        )
    assert str(raised.value) == "DECODER_UNAVAILABLE"
    assert "CANARY" not in str(raised.value)


@pytest.mark.parametrize("failure", ["kill", "job-close", "pipe-close", "thread-start", "join"])
def test_cleanup_faults_attempt_every_remaining_owned_resource(
    monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    calls: list[str] = []

    class Pipe(io.BytesIO):
        def __init__(self, name: str) -> None:
            super().__init__()
            self.name = name

        def close(self) -> None:
            calls.append("close-" + self.name)
            super().close()
            if failure == "pipe-close" and self.name == "stdin":
                raise OSError("PUBLIC-CANARY")

    class Process:
        stdin, stdout, stderr = Pipe("stdin"), Pipe("stdout"), Pipe("stderr")
        returncode = None

        def poll(self) -> None:
            return None

        def kill(self) -> None:
            calls.append("kill")
            if failure == "kill":
                raise OSError("PUBLIC-CANARY")

        def wait(self, timeout: float) -> int:
            assert 0 <= timeout <= 1
            calls.append("wait")
            return 0

    class Job:
        def assign_and_resume(self, process: Any) -> None:
            calls.append("assigned")

        def close(self, deadline: float) -> None:
            calls.append("job-close")
            if failure == "job-close":
                raise cli.DecoderHelperError

    threads: list[Any] = []

    class Thread:
        def __init__(self, **kwargs: Any) -> None:
            self.index = len(threads)
            threads.append(self)

        def start(self) -> None:
            calls.append(f"start-{self.index}")
            if failure == "thread-start" and self.index == 1:
                raise RuntimeError("PUBLIC-CANARY")

        def join(self, timeout: float) -> None:
            assert 0 <= timeout <= 1
            calls.append(f"join-{self.index}")
            if failure == "join" and self.index == 0:
                raise RuntimeError("PUBLIC-CANARY")

        def is_alive(self) -> bool:
            return False

    process = Process()
    monkeypatch.setattr(cli, "_WindowsJob", Job)
    monkeypatch.setattr(cli.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(cli.threading, "Thread", Thread)
    checks = 0

    def cancel_after_assignment() -> bool:
        nonlocal checks
        checks += 1
        return checks > 1

    with pytest.raises(cli.DecoderHelperError) as raised:
        cli.run_owned_cli(
            native_command(""),
            env={},
            deadline=time.monotonic() + 2,
            cleanup_deadline=time.monotonic() + 3,
            source=b"public",
            cancelled=cancel_after_assignment,
        )
    assert str(raised.value) == "DECODER_UNAVAILABLE"
    assert "assigned" in calls and "job-close" in calls and "kill" in calls and "wait" in calls
    assert "join-0" in calls
    if failure != "thread-start":
        assert "join-1" in calls and "join-2" in calls
    assert all("close-" + name in calls for name in ("stdin", "stdout", "stderr"))
    assert all(pipe.closed for pipe in (process.stdin, process.stdout, process.stderr))
