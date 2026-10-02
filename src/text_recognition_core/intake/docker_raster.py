"""Explicit Windows/Docker Desktop raster adapter; no automatic runtime admission."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from text_recognition_core.application.ports import CancellationToken
from text_recognition_core.application.raster import DecodedRaster
from text_recognition_core.intake.envelope import MAX_SOURCE_BYTES, inspect_source_bytes
from text_recognition_core.intake.owned_decoder_cli import DecoderHelperError, run_owned_cli
from text_recognition_core.intake.raster_protocol import (
    MAX_FRAME_BYTES,
    RasterFrameReader,
    RasterProtocolError,
)

_HEX = re.compile(r"[0-9a-f]{64}\Z")
_IMAGE = re.compile(r"sha256:[0-9a-f]{64}\Z")
_LABEL = "org.text-recognition-core.decoder.nonce"
_ENDPOINT = "npipe:////./pipe/dockerDesktopLinuxEngine"
_ENTRYPOINT = ("python", "-I", "-B", "/opt/trc/raster_worker.py")
_TOTAL_SECONDS = 20.0
_CLEANUP_SECONDS = 4.0
_MEMORY = 268435456
_TMPFS = "rw,noexec,nosuid,nodev,size=64m"
_FAILURES = frozenset(
    {
        "DECODER_RUNTIME_UNAVAILABLE",
        "DECODER_INPUT_INVALID",
        "DECODER_INPUT_LIMIT",
        "DECODER_PROFILE_UNSUPPORTED",
        "DECODER_GEOMETRY_LIMIT",
        "DECODER_DECODE_FAILED",
        "DECODER_OUTPUT_LIMIT",
        "DECODER_UNAVAILABLE",
        "DECODER_FAILED",
        "DECODER_TIMEOUT",
        "DECODER_CANCELLED",
    }
)


@dataclass(frozen=True, slots=True)
class DockerRasterBinding:
    """Deployment-owned reviewed artifact facts, never values from a document caller.

    The receipt identifies a separately reviewed actual-runtime/build/license
    admission. This value is not itself a license/security verifier or image builder.
    Runtime never pulls an image, invokes a host decoder, or admits arbitrary tags.
    """

    executable: Path
    executable_sha256: str
    image_id: str
    image_environment: tuple[str, ...]
    admission_receipt_sha256: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.executable, Path)
            or not self.executable.is_absolute()
            or not _HEX.fullmatch(self.executable_sha256)
            or not _IMAGE.fullmatch(self.image_id)
            or not _HEX.fullmatch(self.admission_receipt_sha256)
            or type(self.image_environment) is not tuple
            or not self.image_environment
            or any(type(item) is not str or "=" not in item for item in self.image_environment)
            or len(self.image_environment) > 16
            or sum(len(item) for item in self.image_environment) > 4096
        ):
            raise ValueError("DECODER_UNAVAILABLE")


@dataclass(frozen=True, slots=True)
class OwnedRasterRecovery:
    """Content-free ownership evidence when cleanup cannot be confirmed."""

    image_id: str
    nonce: str
    container_id: str | None


class RasterDecoderError(ValueError):
    def __init__(self, code: str, recovery: OwnedRasterRecovery | None = None) -> None:
        if code not in _FAILURES:
            code = "DECODER_FAILED"
        self.code = code
        self.recovery = recovery
        super().__init__(code)


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RasterDecoderError("DECODER_UNAVAILABLE")
        result[key] = value
    return result


def _deny_constant(_: str) -> Any:
    raise RasterDecoderError("DECODER_UNAVAILABLE")


def _metadata(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_unique, parse_constant=_deny_constant
        )
        if type(value) is not dict:
            raise ValueError
        return value
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise RasterDecoderError("DECODER_UNAVAILABLE") from None


class WindowsDockerRasterDecoder:
    """Synchronous single-invocation adapter with exact owned-container cleanup."""

    def __init__(self, binding: DockerRasterBinding) -> None:
        self._binding = binding
        self._lock = threading.Lock()
        self._pending_recovery: OwnedRasterRecovery | None = None

    @property
    def pending_recovery(self) -> OwnedRasterRecovery | None:
        """Retained ownership evidence; deployment must resolve before replacing this instance."""
        return self._pending_recovery

    def _executable(self) -> str:
        path = self._binding.executable
        try:
            if os.name != "nt" or path.resolve(strict=True) != path or not path.is_file():
                raise ValueError
            # Hash the actual 43MiB signed native CLI in bounded chunks, never one allocation.
            digest = hashlib.sha256()
            count = 0
            with path.open("rb") as stream:
                before = os.fstat(stream.fileno())
                while chunk := stream.read(65536):
                    if count == 0 and not chunk.startswith(b"MZ"):
                        raise ValueError
                    count += len(chunk)
                    if count > 64 * 1024 * 1024:
                        raise ValueError
                    digest.update(chunk)
                after = os.fstat(stream.fileno())
            if (
                count != before.st_size
                or (before.st_size, before.st_mtime_ns, before.st_ino)
                != (after.st_size, after.st_mtime_ns, after.st_ino)
                or digest.hexdigest() != self._binding.executable_sha256
            ):
                raise ValueError
            return str(path)
        except (OSError, ValueError, RuntimeError):
            raise RasterDecoderError("DECODER_UNAVAILABLE") from None

    def _cli(
        self,
        arguments: list[str],
        *,
        config: str,
        deadline: float,
        cleanup_deadline: float,
        cancelled: Any,
        source: bytes | None = None,
        reader: RasterFrameReader | None = None,
    ) -> tuple[int, bytes, bytes, int]:
        executable = self._executable()
        # A new empty config directory excludes credentials/context/plugin settings.
        # Endpoint and every container option below are deployment-owned constants.
        env = {
            key: os.environ[key]
            for key in ("SystemRoot", "WINDIR", "TEMP", "TMP")
            if key in os.environ
        }
        env["PATH"] = str(Path(executable).parent)
        return run_owned_cli(
            [executable, "--config", config, "--host", _ENDPOINT, *arguments],
            env=env,
            deadline=deadline,
            cleanup_deadline=cleanup_deadline,
            cancelled=cancelled,
            source=source,
            stdout_limit=MAX_FRAME_BYTES if reader is not None else 16384,
            stderr_limit=16384,
            combined_limit=None if reader is not None else 16384,
            on_stdout=reader.feed if reader is not None else None,
        )

    @staticmethod
    def _ownership(metadata: dict[str, Any], image_id: str, nonce: str, cid: str) -> bool:
        config = metadata.get("Config")
        return (
            type(config) is dict
            and metadata.get("Id") == cid
            and metadata.get("Image") == image_id
            and type(config.get("Labels")) is dict
            and config["Labels"].get(_LABEL) == nonce
        )

    def _controls(self, data: dict[str, Any], nonce: str, cid: str) -> None:
        try:
            config, host = data["Config"], data["HostConfig"]
            limits = host["Ulimits"]
            state = data["State"]
            valid = (
                self._ownership(data, self._binding.image_id, nonce, cid)
                and config["Image"] == self._binding.image_id
                and tuple(config["Entrypoint"]) == _ENTRYPOINT
                and not config["Cmd"]
                and config["User"] == "65532:65532"
                and config["WorkingDir"] == "/opt/trc"
                and tuple(config["Env"]) == self._binding.image_environment
                and config["Labels"] == {_LABEL: nonce}
                and config["Tty"] is False
                and config["OpenStdin"] is True
                and config["AttachStdin"] is True
                and config["AttachStdout"] is True
                and config["AttachStderr"] is True
                and not config["Volumes"]
                and not config.get("ExposedPorts")
                and data["NetworkSettings"]["Ports"] == {}
                and data["Path"] == "python"
                and tuple(data["Args"]) == _ENTRYPOINT[1:]
                and data["Mounts"] == []
                and host["ReadonlyRootfs"] is True
                and host["Privileged"] is False
                and host["CapDrop"] == ["ALL"]
                and not host["CapAdd"]
                and host["SecurityOpt"] == ["no-new-privileges"]
                and host["NetworkMode"] == "none"
                and host["IpcMode"] == "private"
                and not host["PidMode"]
                and not host["UTSMode"]
                and not host["Binds"]
                and not host.get("Mounts")
                and not host["Devices"]
                and not host["DeviceRequests"]
                and not host["DeviceCgroupRules"]
                and not host["VolumesFrom"]
                and not host["PortBindings"]
                and host["PublishAllPorts"] is False
                and host["Memory"] == _MEMORY
                and type(host["Memory"]) is int
                and host["MemorySwap"] == _MEMORY
                and type(host["MemorySwap"]) is int
                and host["NanoCpus"] == 1000000000
                and type(host["NanoCpus"]) is int
                and host["PidsLimit"] == 8
                and type(host["PidsLimit"]) is int
                and host["Tmpfs"] == {"/tmp": _TMPFS}
                and host["LogConfig"] == {"Type": "none", "Config": {}}
                and sorted(limits, key=lambda value: value["Name"])
                == [
                    {"Name": "fsize", "Hard": 67108864, "Soft": 67108864},
                    {"Name": "nofile", "Hard": 32, "Soft": 32},
                ]
                and state["Running"] is False
                and state["Status"] == "created"
            )
        except (KeyError, TypeError, ValueError):
            valid = False
        if not valid:
            raise RasterDecoderError("DECODER_UNAVAILABLE")

    def decode(self, source: bytes, cancellation: CancellationToken) -> DecodedRaster:
        started = time.monotonic()
        total_deadline = started + _TOTAL_SECONDS
        processing_deadline = total_deadline - _CLEANUP_SECONDS
        if type(source) is not bytes or not 0 < len(source) <= MAX_SOURCE_BYTES:
            raise RasterDecoderError("DECODER_INPUT_LIMIT")
        try:
            envelope = inspect_source_bytes(io.BytesIO(source))
        except ValueError:
            raise RasterDecoderError("DECODER_INPUT_INVALID") from None
        if envelope.kind == "pdf":
            raise RasterDecoderError("DECODER_PROFILE_UNSUPPORTED")
        if not self._lock.acquire(blocking=False):
            raise RasterDecoderError("DECODER_UNAVAILABLE")
        nonce = uuid.uuid4().hex
        cid: str | None = None
        creation_attempted = False
        result: DecodedRaster | None = None
        try:
            if self._pending_recovery is not None:
                raise RasterDecoderError("DECODER_UNAVAILABLE", self._pending_recovery)
            with tempfile.TemporaryDirectory(prefix="trc-decoder-cli-") as config:

                def call(
                    arguments: list[str], *, cleanup: bool = False, **kwargs: Any
                ) -> tuple[int, bytes, bytes, int]:
                    return self._cli(
                        arguments,
                        config=config,
                        deadline=total_deadline if cleanup else processing_deadline,
                        cleanup_deadline=total_deadline,
                        cancelled=(lambda: False) if cleanup else cancellation.cancelled,
                        **kwargs,
                    )

                def metadata(arguments: list[str], *, cleanup: bool = False) -> dict[str, Any]:
                    code, output, errors, _ = call(arguments, cleanup=cleanup)
                    if code != 0 or errors:
                        raise RasterDecoderError("DECODER_UNAVAILABLE")
                    return _metadata(output)

                def discover() -> str | None:
                    code, output, errors, _ = call(
                        ["ps", "-a", "-q", "--no-trunc", "--filter", f"label={_LABEL}={nonce}"],
                        cleanup=True,
                    )
                    if code != 0 or errors:
                        raise RasterDecoderError("DECODER_UNAVAILABLE")
                    try:
                        ids = output.decode("ascii").splitlines()
                    except UnicodeError:
                        raise RasterDecoderError("DECODER_UNAVAILABLE") from None
                    if len(ids) > 1 or any(not _HEX.fullmatch(value) for value in ids):
                        raise RasterDecoderError("DECODER_UNAVAILABLE")
                    return ids[0] if ids else None

                try:
                    image = metadata(
                        ["image", "inspect", self._binding.image_id, "--format", "{{json .}}"]
                    )
                    image_config = image.get("Config")
                    if (
                        image.get("Id") != self._binding.image_id
                        or image.get("Os") != "linux"
                        or image.get("Architecture") != "amd64"
                        or type(image_config) is not dict
                        or type(image_config.get("Env")) is not list
                        or tuple(image_config["Env"]) != self._binding.image_environment
                    ):
                        raise RasterDecoderError("DECODER_UNAVAILABLE")
                    creation_attempted = True
                    code, output, errors, _ = call(
                        [
                            "create",
                            "--pull=never",
                            "--platform",
                            "linux/amd64",
                            "-i",
                            "--label",
                            f"{_LABEL}={nonce}",
                            "--network",
                            "none",
                            "--ipc",
                            "private",
                            "--read-only",
                            "--user",
                            "65532:65532",
                            "--cap-drop",
                            "ALL",
                            "--security-opt",
                            "no-new-privileges",
                            "--memory",
                            "256m",
                            "--memory-swap",
                            "256m",
                            "--cpus",
                            "1",
                            "--pids-limit",
                            "8",
                            "--ulimit",
                            "nofile=32:32",
                            "--ulimit",
                            "fsize=67108864:67108864",
                            "--tmpfs",
                            f"/tmp:{_TMPFS}",
                            "--log-driver",
                            "none",
                            self._binding.image_id,
                        ]
                    )
                    try:
                        candidate = output.decode("ascii").strip()
                    except UnicodeError:
                        candidate = ""
                    if code != 0 or errors or not _HEX.fullmatch(candidate):
                        raise RasterDecoderError("DECODER_UNAVAILABLE")
                    cid = candidate
                    data = metadata(["inspect", cid, "--format", "{{json .}}"])
                    self._controls(data, nonce, cid)
                    reader = RasterFrameReader(envelope)
                    code, _, errors, sent = call(
                        ["start", "-a", "-i", cid], source=source, reader=reader
                    )
                    if code != 0:
                        fixed = errors.decode("ascii", errors="ignore").rstrip("\n")
                        if fixed in _FAILURES and errors == (fixed + "\n").encode("ascii"):
                            raise RasterDecoderError(fixed)
                        raise RasterDecoderError("DECODER_FAILED")
                    if errors or sent != envelope.byte_count:
                        raise RasterDecoderError("DECODER_FAILED")
                    state = metadata(["inspect", cid, "--format", "{{json .}}"])["State"]
                    if (
                        state["Running"] is not False
                        or state["Status"] != "exited"
                        or type(state["ExitCode"]) is not int
                        or state["ExitCode"] != 0
                        or state["OOMKilled"] is not False
                        or state["Error"]
                    ):
                        raise RasterDecoderError("DECODER_FAILED")
                    result = reader.finish()
                except DecoderHelperError:
                    if cancellation.cancelled():
                        raise RasterDecoderError("DECODER_CANCELLED") from None
                    if time.monotonic() >= processing_deadline:
                        raise RasterDecoderError("DECODER_TIMEOUT") from None
                    raise RasterDecoderError("DECODER_UNAVAILABLE") from None
                except (RasterProtocolError, KeyError, TypeError, UnicodeError):
                    raise RasterDecoderError("DECODER_FAILED") from None
                finally:
                    if creation_attempted:
                        try:
                            observed = discover()
                            # Killing a local helper does not cancel an already-sent daemon request.
                            # With no acknowledged/discovered CID, a finite empty scan cannot prove
                            # absence of a late creation. Preserve nonce recovery and deny success.
                            if cid is None and observed is None:
                                raise RasterDecoderError("DECODER_UNAVAILABLE")
                            if cid is not None and observed != cid:
                                raise RasterDecoderError("DECODER_UNAVAILABLE")
                            if observed is not None:
                                cid = observed
                                data = metadata(
                                    ["inspect", cid, "--format", "{{json .}}"], cleanup=True
                                )
                                if not self._ownership(data, self._binding.image_id, nonce, cid):
                                    raise RasterDecoderError("DECODER_UNAVAILABLE")
                                code, _, errors, _ = call(["rm", "-f", cid], cleanup=True)
                                if code != 0 or errors or discover() is not None:
                                    raise RasterDecoderError("DECODER_UNAVAILABLE")
                        except BaseException as interruption:
                            # An interrupted proof is unknown, even for task cancellation or Ctrl+C.
                            self._pending_recovery = OwnedRasterRecovery(
                                self._binding.image_id, nonce, cid
                            )
                            if not isinstance(interruption, Exception):
                                raise
                            raise RasterDecoderError(
                                "DECODER_UNAVAILABLE", self._pending_recovery
                            ) from None
            if cancellation.cancelled():
                raise RasterDecoderError("DECODER_CANCELLED")
            if result is None or time.monotonic() >= total_deadline:
                raise RasterDecoderError("DECODER_UNAVAILABLE")
            return result
        except OSError:
            raise RasterDecoderError("DECODER_UNAVAILABLE") from None
        finally:
            self._lock.release()
