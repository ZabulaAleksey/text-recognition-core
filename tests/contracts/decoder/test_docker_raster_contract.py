from __future__ import annotations

import copy
import hashlib
import json
import struct
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest

from text_recognition_core.intake import docker_raster as raster
from text_recognition_core.intake.owned_decoder_cli import DecoderHelperError

_ACTUAL_METADATA = {
    "HostConfig": {
        "ReadonlyRootfs": True,
        "Privileged": False,
        "CapDrop": ["ALL"],
        "CapAdd": None,
        "SecurityOpt": ["no-new-privileges"],
        "NetworkMode": "none",
        "IpcMode": "private",
        "PidMode": "",
        "UTSMode": "",
        "Binds": None,
        "Devices": [],
        "DeviceRequests": None,
        "DeviceCgroupRules": None,
        "VolumesFrom": None,
        "PortBindings": {},
        "PublishAllPorts": False,
        "Memory": 268435456,
        "MemorySwap": 268435456,
        "NanoCpus": 1000000000,
        "PidsLimit": 8,
        "Tmpfs": {"/tmp": "rw,noexec,nosuid,nodev,size=64m"},
        "LogConfig": {"Type": "none", "Config": {}},
        "Ulimits": [
            {"Name": "fsize", "Hard": 67108864, "Soft": 67108864},
            {"Name": "nofile", "Hard": 32, "Soft": 32},
        ],
    },
    "Config": {
        "Image": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "Entrypoint": ["python", "-I", "-B", "/opt/trc/raster_worker.py"],
        "Cmd": None,
        "User": "65532:65532",
        "WorkingDir": "/opt/trc",
        "Env": [
            "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305",
            "PYTHON_VERSION=3.13.16",
            "PYTHON_SHA256=f4b1bfb3c79b5bb11b8d228a12504163b4c0dab4d679828d8f5f26b6cb6ab35d",
            "PYTHONDONTWRITEBYTECODE=1",
            "PYTHONUNBUFFERED=1",
        ],
        "Labels": {"org.text-recognition-core.decoder.nonce": "cccccccccccccccccccccccccccccccc"},
        "Tty": False,
        "OpenStdin": True,
        "AttachStdin": True,
        "AttachStdout": True,
        "AttachStderr": True,
        "Volumes": None,
    },
    "Path": "python",
    "Args": ["-I", "-B", "/opt/trc/raster_worker.py"],
    "Mounts": [],
    "NetworkSettings": {"Ports": {}},
    "State": {
        "Running": False,
        "Status": "created",
        "ExitCode": 0,
        "OOMKilled": False,
        "Error": "",
    },
    "Id": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "Image": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
}
IMAGE = "sha256:" + "a" * 64
CID = "b" * 64
NONCE = "c" * 32
SOURCE = b"\x89PNG\r\n\x1a\npublic-envelope-only"
PIXELS = bytes((12, 34, 56))


class Token:
    stopped = False

    def cancelled(self) -> bool:
        return self.stopped


def binding() -> raster.DockerRasterBinding:
    return raster.DockerRasterBinding(
        Path(__file__).resolve(),
        "d" * 64,
        IMAGE,
        tuple(_ACTUAL_METADATA["Config"]["Env"]),
        "e" * 64,
    )


def metadata() -> dict[str, Any]:
    return copy.deepcopy(_ACTUAL_METADATA)


def frame(source: bytes = SOURCE) -> bytes:
    header = json.dumps(
        {
            "schema": 1,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "kind": "png",
            "width": 1,
            "height": 1,
            "pixel_format": "RGB8",
            "pixel_bytes": 3,
            "pixel_sha256": hashlib.sha256(PIXELS).hexdigest(),
        }
    ).encode()
    return b"TRCRASTER1\n" + struct.pack(">I", len(header)) + header + PIXELS


def test_actual_metadata_optional_empty_fields_are_absent_and_still_admitted() -> None:
    data = metadata()
    assert "Mounts" not in data["HostConfig"]
    assert "ExposedPorts" not in data["Config"]
    raster.WindowsDockerRasterDecoder(binding())._controls(data, NONCE, CID)


@pytest.mark.parametrize(
    "section,key,value",
    [
        ("HostConfig", "ReadonlyRootfs", 1),
        ("HostConfig", "Privileged", 0),
        ("HostConfig", "Memory", True),
        ("HostConfig", "MemorySwap", 268435456.0),
        ("HostConfig", "NanoCpus", 1000000000.0),
        ("HostConfig", "PidsLimit", 8.0),
        ("HostConfig", "NetworkMode", "host"),
        ("HostConfig", "IpcMode", "host"),
        ("HostConfig", "PidMode", "host"),
        ("HostConfig", "UTSMode", "host"),
        ("HostConfig", "Binds", ["/private:/source"]),
        ("HostConfig", "Mounts", [{"Source": "/private", "Target": "/source"}]),
        ("HostConfig", "Devices", [{"PathOnHost": "/dev/private"}]),
        ("HostConfig", "DeviceRequests", [{"Count": -1}]),
        ("HostConfig", "PortBindings", {"80/tcp": [{"HostPort": "8080"}]}),
        ("HostConfig", "PublishAllPorts", True),
        ("HostConfig", "CapAdd", ["SYS_ADMIN"]),
        ("HostConfig", "CapDrop", []),
        ("HostConfig", "SecurityOpt", []),
        ("HostConfig", "Tmpfs", {"/tmp": "rw,exec,size=64m"}),
        ("HostConfig", "LogConfig", {"Type": "json-file", "Config": {}}),
        ("HostConfig", "Ulimits", []),
        ("Config", "User", "0:0"),
        ("Config", "WorkingDir", "/private"),
        ("Config", "Env", ["TOKEN=PUBLIC-CANARY"]),
        ("Config", "ExposedPorts", {"80/tcp": {}}),
        ("Config", "Entrypoint", ["sh"]),
        ("Config", "Cmd", ["caller-command"]),
        ("Config", "Tty", 0),
        ("Config", "OpenStdin", 1),
        ("Config", "Volumes", {"/source": {}}),
        ("NetworkSettings", "Ports", {"80/tcp": None}),
        ("State", "Running", 0),
        ("State", "Status", "running"),
    ],
)
def test_tampered_runtime_controls_deny_before_source_transfer(
    section: str,
    key: str,
    value: Any,
) -> None:
    data = metadata()
    data[section][key] = value
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$"):
        raster.WindowsDockerRasterDecoder(binding())._controls(data, NONCE, CID)


@pytest.mark.parametrize(
    "path",
    [
        ("HostConfig", "ReadonlyRootfs"),
        ("HostConfig", "Privileged"),
        ("HostConfig", "Memory"),
        ("HostConfig", "MemorySwap"),
        ("HostConfig", "NanoCpus"),
        ("HostConfig", "PidsLimit"),
        ("HostConfig", "NetworkMode"),
        ("HostConfig", "Devices"),
        ("Config", "User"),
        ("Config", "Entrypoint"),
        ("Config", "Env"),
        ("NetworkSettings", "Ports"),
        ("State", "Running"),
    ],
)
def test_missing_required_control_is_unavailable(path: tuple[str, str]) -> None:
    data = metadata()
    del data[path[0]][path[1]]
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$"):
        raster.WindowsDockerRasterDecoder(binding())._controls(data, NONCE, CID)


def test_authoritative_host_mounts_required_and_nonempty_denied() -> None:
    decoder = raster.WindowsDockerRasterDecoder(binding())
    for replacement in (None, [{"Source": "/private"}]):
        data = metadata()
        data["Mounts"] = replacement
        with pytest.raises(raster.RasterDecoderError):
            decoder._controls(data, NONCE, CID)
    data = metadata()
    del data["Mounts"]
    with pytest.raises(raster.RasterDecoderError):
        decoder._controls(data, NONCE, CID)


class Scenario:
    def __init__(self, monkeypatch: pytest.MonkeyPatch, failure: str = "") -> None:
        self.decoder = raster.WindowsDockerRasterDecoder(binding())
        self.failure = failure
        self.token = Token()
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.created = self.started = self.removed = False
        monkeypatch.setattr(raster.uuid, "uuid4", lambda: type("Nonce", (), {"hex": NONCE})())
        monkeypatch.setattr(raster.time, "monotonic", lambda: 100.0)
        monkeypatch.setattr(self.decoder, "_cli", self.call)

    def call(self, arguments: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        action = arguments[0]
        cleanup = kwargs["deadline"] == 120.0
        phase = "state" if action == "inspect" and self.started and not cleanup else action
        self.calls.append((phase, {**kwargs, "arguments": arguments}))
        if action == "create":
            self.created = True
        if self.failure == "cancel-" + phase and not cleanup:
            self.token.stopped = True
            raise DecoderHelperError
        if action == "image":
            return (
                0,
                json.dumps(
                    {
                        "Id": IMAGE,
                        "Os": "linux",
                        "Architecture": "amd64",
                        "Config": {"Env": binding().image_environment},
                    }
                ).encode(),
                b"",
                0,
            )
        if action == "create":
            if self.failure == "ambiguous-create":
                return 1, b"PUBLIC-CANARY", b"PUBLIC-CANARY", 0
            return 0, CID.encode() + b"\n", b"", 0
        if action == "inspect":
            data = metadata()
            if self.failure == "foreign-nonce":
                data["Config"]["Labels"] = {raster._LABEL: "f" * 32}
            if self.started:
                data["State"].update(Status="exited", Running=False, ExitCode=0)
                if self.failure == "status-nonzero":
                    data["State"]["ExitCode"] = 1
            return 0, json.dumps(data).encode(), b"", 0
        if action == "start":
            self.started = True
            assert kwargs["source"] == SOURCE
            raw = (
                frame(b"\x89PNG\r\n\x1a\nwrong-source")
                if self.failure == "wrong-source"
                else frame()
            )
            kwargs["reader"].feed(raw)
            if self.failure == "helper-nonzero":
                return 1, b"", b"PUBLIC-CANARY\n", len(SOURCE)
            return 0, b"", b"", len(SOURCE)
        if action == "ps":
            if self.failure == "ambiguous-create":
                return 0, (CID + "\n" + "f" * 64 + "\n").encode(), b"", 0
            return 0, (CID + "\n").encode() if self.created and not self.removed else b"", b"", 0
        if action == "rm":
            assert arguments == ["rm", "-f", CID]
            if self.failure == "cleanup":
                return 1, b"", b"PUBLIC-CANARY", 0
            self.removed = True
            return 0, b"", b"", 0
        raise AssertionError("unexpected fake boundary call")


def test_valid_parent_result_requires_cleanup_and_uses_one_absolute_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario = Scenario(monkeypatch)
    result = scenario.decoder.decode(SOURCE, scenario.token)
    assert result.pixels == PIXELS and result.source_sha256 == hashlib.sha256(SOURCE).hexdigest()
    assert scenario.removed
    assert {kwargs["cleanup_deadline"] for _, kwargs in scenario.calls} == {120.0}
    assert {kwargs["deadline"] for _, kwargs in scenario.calls} == {116.0, 120.0}
    assert scenario.calls[-1][0] == "ps"
    created = next(kwargs["arguments"] for phase, kwargs in scenario.calls if phase == "create")
    assert "--pull=never" in created and created[-1] == IMAGE


@pytest.mark.parametrize("failure", ["wrong-source", "helper-nonzero", "status-nonzero", "cleanup"])
def test_self_consistent_frame_never_escapes_failed_parent_or_cleanup(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    scenario = Scenario(monkeypatch, failure)
    with pytest.raises(raster.RasterDecoderError) as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert "CANARY" not in str(raised.value)
    assert scenario.removed == (failure != "cleanup")
    if failure == "cleanup":
        assert raised.value.code == "DECODER_UNAVAILABLE"
        assert raised.value.recovery == raster.OwnedRasterRecovery(IMAGE, NONCE, CID)


@pytest.mark.parametrize("failure", ["ambiguous-create", "foreign-nonce"])
def test_ambiguous_or_foreign_resource_is_preserved_without_wrong_removal(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    scenario = Scenario(monkeypatch, failure)
    with pytest.raises(raster.RasterDecoderError) as raised:
        scenario.decoder.decode(SOURCE, scenario.token)
    assert raised.value.code == "DECODER_UNAVAILABLE" and raised.value.recovery is not None
    assert not any(phase == "rm" for phase, _ in scenario.calls)
    assert not scenario.removed


@pytest.mark.parametrize("phase", ["image", "create", "inspect", "start", "state"])
def test_phase_cancellation_discards_result_but_cleanup_is_never_cancelled(
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    scenario = Scenario(monkeypatch, "cancel-" + phase)
    with pytest.raises(raster.RasterDecoderError, match="^DECODER_CANCELLED$"):
        scenario.decoder.decode(SOURCE, scenario.token)
    cleanup = [kwargs for _, kwargs in scenario.calls if kwargs["deadline"] == 120.0]
    assert all(kwargs["cancelled"]() is False for kwargs in cleanup)
    assert scenario.removed == (phase != "image")
    assert all(kwargs["cleanup_deadline"] == 120.0 for _, kwargs in scenario.calls)


def test_adapter_refuses_concurrent_admission_without_any_cli_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario = Scenario(monkeypatch)
    scenario.decoder._lock.acquire()
    try:
        with pytest.raises(raster.RasterDecoderError, match="^DECODER_UNAVAILABLE$"):
            scenario.decoder.decode(SOURCE, scenario.token)
        assert scenario.calls == []
    finally:
        scenario.decoder._lock.release()


def test_cli_endpoint_environment_and_caps_are_deployment_owned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    decoder = raster.WindowsDockerRasterDecoder(binding())
    monkeypatch.setattr(decoder, "_executable", lambda: str(Path(__file__).resolve()))
    monkeypatch.setenv("PUBLIC_CALLER_TOKEN", "PUBLIC-CANARY")
    observed: dict[str, Any] = {}

    def helper(argv: list[str], **kwargs: Any) -> tuple[int, bytes, bytes, int]:
        observed.update(argv=argv, **kwargs)
        return 0, b"", b"", 0

    monkeypatch.setattr(raster, "run_owned_cli", helper)
    decoder._cli(
        ["image", "inspect", IMAGE],
        config="empty-owned-config",
        deadline=116.0,
        cleanup_deadline=120.0,
        cancelled=lambda: False,
    )
    assert observed["argv"][1:5] == ["--config", "empty-owned-config", "--host", raster._ENDPOINT]
    assert "PUBLIC_CALLER_TOKEN" not in observed["env"]
    assert (
        observed["stdout_limit"] == observed["stderr_limit"] == observed["combined_limit"] == 16384
    )
    assert observed["deadline"] == 116.0 and observed["cleanup_deadline"] == 120.0


def test_binding_is_immutable_and_rejects_mutable_tags() -> None:
    deployment = binding()
    with pytest.raises(FrozenInstanceError):
        deployment.image_id = "python:latest"  # type: ignore[misc]
    with pytest.raises(ValueError, match="^DECODER_UNAVAILABLE$"):
        raster.DockerRasterBinding(
            deployment.executable, "d" * 64, "python:latest", deployment.image_environment, "e" * 64
        )
