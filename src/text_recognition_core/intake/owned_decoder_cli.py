"""Owned native Docker helper, bounded pipes; no shell or caller command surface."""

from __future__ import annotations

import ctypes
import os
import queue
import subprocess
import threading
import time
from collections.abc import Callable, Mapping
from ctypes import wintypes


class DecoderHelperError(ValueError):
    def __init__(self) -> None:
        super().__init__("DECODER_UNAVAILABLE")


class _BasicLimits(ctypes.Structure):
    _fields_ = [
        ("user_time", ctypes.c_longlong),
        ("job_time", ctypes.c_longlong),
        ("flags", wintypes.DWORD),
        ("min_ws", ctypes.c_size_t),
        ("max_ws", ctypes.c_size_t),
        ("active_limit", wintypes.DWORD),
        ("affinity", ctypes.c_size_t),
        ("priority", wintypes.DWORD),
        ("scheduling", wintypes.DWORD),
    ]


class _IoCounters(ctypes.Structure):
    _fields_ = [(f"counter{i}", ctypes.c_ulonglong) for i in range(6)]


class _ExtendedLimits(ctypes.Structure):
    _fields_ = [
        ("basic", _BasicLimits),
        ("io", _IoCounters),
        ("process_memory", ctypes.c_size_t),
        ("job_memory", ctypes.c_size_t),
        ("peak_process", ctypes.c_size_t),
        ("peak_job", ctypes.c_size_t),
    ]


class _ThreadEntry(ctypes.Structure):
    _fields_ = [
        ("size", wintypes.DWORD),
        ("usage", wintypes.DWORD),
        ("tid", wintypes.DWORD),
        ("pid", wintypes.DWORD),
        ("priority", wintypes.LONG),
        ("delta", wintypes.LONG),
        ("flags", wintypes.DWORD),
    ]


class _JobAccounting(ctypes.Structure):
    _fields_ = [
        ("user", ctypes.c_longlong),
        ("kernel", ctypes.c_longlong),
        ("period_user", ctypes.c_longlong),
        ("period_kernel", ctypes.c_longlong),
        ("faults", wintypes.DWORD),
        ("processes", wintypes.DWORD),
        ("active", wintypes.DWORD),
        ("terminated", wintypes.DWORD),
    ]


class _WindowsJob:
    def __init__(self) -> None:
        self._kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        api = self._kernel
        api.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        api.CreateJobObjectW.restype = wintypes.HANDLE
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        api.CloseHandle.restype = wintypes.BOOL
        self._handle = api.CreateJobObjectW(None, None)
        if not self._handle:
            raise DecoderHelperError
        info = _ExtendedLimits()
        info.basic.flags = 0x2000  # KILL_ON_JOB_CLOSE
        api.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        if not api.SetInformationJobObject(
            self._handle, 9, ctypes.byref(info), ctypes.sizeof(info)
        ):
            api.CloseHandle(self._handle)
            self._handle = None
            raise DecoderHelperError

    def assign_and_resume(self, process: subprocess.Popen[bytes]) -> None:
        api = self._kernel
        api.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        handle = wintypes.HANDLE(int(process._handle))  # type: ignore[attr-defined]
        if not api.AssignProcessToJobObject(self._handle, handle):
            raise DecoderHelperError
        api.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        api.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        snapshot = api.CreateToolhelp32Snapshot(4, 0)
        if snapshot in (None, ctypes.c_void_p(-1).value):
            raise DecoderHelperError
        api.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry)]
        api.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry)]
        entry = _ThreadEntry()
        entry.size = ctypes.sizeof(entry)
        threads: list[int] = []
        try:
            present = api.Thread32First(snapshot, ctypes.byref(entry))
            while present:
                if entry.pid == process.pid:
                    threads.append(entry.tid)
                present = api.Thread32Next(snapshot, ctypes.byref(entry))
        finally:
            api.CloseHandle(snapshot)
        if len(threads) != 1 or process.poll() is not None:
            raise DecoderHelperError
        api.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        api.OpenThread.restype = wintypes.HANDLE
        # Query-limited-information + suspend/resume, exact suspended process thread.
        thread = api.OpenThread(0x0802, False, threads[0])
        if not thread:
            raise DecoderHelperError
        api.GetProcessIdOfThread.argtypes = [wintypes.HANDLE]
        api.GetProcessIdOfThread.restype = wintypes.DWORD
        api.ResumeThread.argtypes = [wintypes.HANDLE]
        api.ResumeThread.restype = wintypes.DWORD
        try:
            if api.GetProcessIdOfThread(thread) != process.pid or process.poll() is not None:
                raise DecoderHelperError
            if api.ResumeThread(thread) != 1:
                raise DecoderHelperError
        finally:
            api.CloseHandle(thread)

    def close(self, deadline: float) -> None:
        if self._handle:
            handle = self._handle
            self._handle = None
            api = self._kernel
            api.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
            api.QueryInformationJobObject.argtypes = [
                wintypes.HANDLE,
                ctypes.c_int,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.c_void_p,
            ]
            failed = False
            try:
                if not api.TerminateJobObject(handle, 1):
                    raise DecoderHelperError
                while True:
                    accounting = _JobAccounting()
                    if not api.QueryInformationJobObject(
                        handle, 1, ctypes.byref(accounting), ctypes.sizeof(accounting), None
                    ):
                        raise DecoderHelperError
                    if accounting.active == 0:
                        break
                    if time.monotonic() >= deadline:
                        raise DecoderHelperError
                    time.sleep(min(0.005, deadline - time.monotonic()))
            except DecoderHelperError:
                failed = True
            finally:
                if not api.CloseHandle(handle):
                    failed = True
            if failed:
                raise DecoderHelperError


def run_owned_cli(
    argv: list[str],
    *,
    env: Mapping[str, str],
    deadline: float,
    cancelled: Callable[[], bool],
    source: bytes | None = None,
    stdout_limit: int = 16384,
    stderr_limit: int = 16384,
    combined_limit: int | None = 16384,
    cleanup_deadline: float | None = None,
    on_stdout: Callable[[bytes], None] | None = None,
) -> tuple[int, bytes, bytes, int]:
    """Windows profile: one Job owns helpers before resume, with bounded concurrent I/O."""
    if os.name != "nt":
        # A POSIX process group alone does not prove containment after descendant setsid().
        raise DecoderHelperError
    process: subprocess.Popen[bytes] | None = None
    job: _WindowsJob | None = None
    stopped = threading.Event()
    events: queue.Queue[tuple[str, bytes | int | None]] = queue.Queue(maxsize=16)
    threads: list[threading.Thread] = []
    output = bytearray()
    errors = bytearray()
    sent = 0
    combined_count = 0
    count_lock = threading.Lock()
    exited_streams: set[str] = set()

    def deliver(kind: str, value: bytes | int | None) -> None:
        while not stopped.is_set():
            try:
                events.put((kind, value), timeout=0.02)
                return
            except queue.Full:
                continue

    def drain(kind: str, stream: object, cap: int) -> None:
        nonlocal combined_count
        count = 0
        try:
            while not stopped.is_set():
                chunk = stream.read(65536)  # type: ignore[attr-defined]
                if not chunk:
                    deliver(kind, None)
                    return
                count += len(chunk)
                with count_lock:
                    combined_count += len(chunk)
                    exceeded = combined_limit is not None and combined_count > combined_limit
                if count > cap or exceeded:
                    deliver("failure", None)
                    return
                deliver(kind, chunk)
        except (OSError, ValueError):
            deliver("failure", None)

    def write_input() -> None:
        assert process is not None and process.stdin is not None and source is not None
        position = 0
        try:
            while position < len(source) and not stopped.is_set():
                written = process.stdin.write(source[position : position + 65536])
                if type(written) is not int or written <= 0:
                    raise OSError
                position += written
            process.stdin.close()
            deliver("sent", position)
        except (OSError, ValueError):
            deliver("failure", None)

    try:
        if time.monotonic() >= deadline or cancelled():
            raise DecoderHelperError
        job = _WindowsJob()
        process = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE if source is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(env),
            cwd=os.path.dirname(argv[0]),
            shell=False,
            close_fds=True,
            bufsize=0,
            # CREATE_SUSPENDED + CREATE_NO_WINDOW before Job assignment/ResumeThread.
            creationflags=0x08000004,
        )
        if job is not None:
            job.assign_and_resume(process)
        for kind, pipe, limit in (
            ("stdout", process.stdout, stdout_limit),
            ("stderr", process.stderr, stderr_limit),
        ):
            thread = threading.Thread(target=drain, args=(kind, pipe, limit), daemon=True)
            thread.start()
            threads.append(thread)
        if source is not None:
            thread = threading.Thread(target=write_input, daemon=True)
            thread.start()
            threads.append(thread)
        while True:
            if time.monotonic() >= deadline or cancelled():
                raise DecoderHelperError
            if (
                len(exited_streams) == 2
                and (source is None or sent == len(source))
                and process.poll() is not None
            ):
                code = process.returncode
                assert isinstance(code, int)
                return code, bytes(output), bytes(errors), sent
            try:
                kind, value = events.get(timeout=min(0.02, max(0.001, deadline - time.monotonic())))
            except queue.Empty:
                continue
            if kind == "failure":
                raise DecoderHelperError
            if kind == "sent":
                assert type(value) is int
                sent = value
            elif value is None:
                exited_streams.add(kind)
            elif kind == "stdout":
                assert type(value) is bytes
                if on_stdout is not None:
                    on_stdout(value)
                else:
                    output.extend(value)
            elif kind == "stderr":
                assert type(value) is bytes
                errors.extend(value)
    except (OSError, RuntimeError, subprocess.SubprocessError):
        raise DecoderHelperError from None
    finally:
        stopped.set()
        cleanup_end = deadline if cleanup_deadline is None else cleanup_deadline
        cleanup_failed = False
        cleanup_interruption: BaseException | None = None

        def remember_cleanup_error(error: BaseException) -> None:
            nonlocal cleanup_failed, cleanup_interruption
            cleanup_failed = True
            if not isinstance(error, Exception) and cleanup_interruption is None:
                cleanup_interruption = error

        # Job kill stops helper descendants and unblocks every pipe.
        if job is not None:
            try:
                job.close(cleanup_end)
            except BaseException as error:
                remember_cleanup_error(error)
        if process is not None:
            try:
                if process.poll() is None:
                    process.kill()
            except BaseException as error:
                remember_cleanup_error(error)
            try:
                process.wait(timeout=max(0, min(1, cleanup_end - time.monotonic())))
            except BaseException as error:
                remember_cleanup_error(error)
        for thread in threads:
            try:
                thread.join(timeout=max(0, min(1, cleanup_end - time.monotonic())))
            except BaseException as error:
                remember_cleanup_error(error)
        for thread in threads:
            try:
                if thread.is_alive():
                    cleanup_failed = True
            except BaseException as error:
                remember_cleanup_error(error)
        if process is not None:
            for pipe in (process.stdin, process.stdout, process.stderr):
                if pipe is not None:
                    try:
                        pipe.close()
                    except BaseException as error:
                        remember_cleanup_error(error)
        if cleanup_interruption is not None:
            raise cleanup_interruption
        if cleanup_failed:
            raise DecoderHelperError
