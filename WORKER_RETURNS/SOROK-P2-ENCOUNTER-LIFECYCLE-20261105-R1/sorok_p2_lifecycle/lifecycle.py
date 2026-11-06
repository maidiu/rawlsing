"""Persistent local encounter lifecycle around the accepted S45 projection."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from . import runtime

SCHEMA = "SOROK_P2_LOCAL_ENCOUNTER_LIFECYCLE@1"
RESULT_SCHEMA = "SOROK_P2_LOCAL_LIFECYCLE_RESULT@1"
GRADE = "TEST_ONLY_LOCAL_UI_LIFECYCLE_NOT_NATIVE"
LOCAL_DIR = ".sorok_p2_local"
STATE_NAME = "encounter_lifecycle.json"
MODES = frozenset({"PORTAL", "OUTSIDE"})
BLOCKED_CODE = "LOCAL_OUTSIDE_MODE_BLOCKED"
RETURN_CODE = "LOCAL_RETURN_ONLY"


class LifecycleRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def local_state_path(state_root) -> Path:
    return Path(state_root) / LOCAL_DIR / STATE_NAME


def _default_state() -> dict:
    return {"mode": "PORTAL", "sequence": 0, "last_action": ""}


def _public_state(state: Mapping[str, Any]) -> dict:
    return {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "mode": state["mode"],
        "sequence": state["sequence"],
        "last_action": state["last_action"],
        "local_only": True,
        "world_event_created": False,
        "clock_changed": False,
    }


def _load_local_state(state_root) -> dict | None:
    path = local_state_path(state_root)
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleRefusal("LOCAL_LIFECYCLE_STATE_UNREADABLE", str(exc)) from exc
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise LifecycleRefusal("LOCAL_LIFECYCLE_SCHEMA_INVALID")
    if value.get("mode") not in MODES:
        raise LifecycleRefusal("LOCAL_LIFECYCLE_MODE_INVALID", str(value.get("mode")))
    if not isinstance(value.get("sequence"), int) or value["sequence"] < 0:
        raise LifecycleRefusal("LOCAL_LIFECYCLE_SEQUENCE_INVALID")
    if not isinstance(value.get("last_action"), str):
        raise LifecycleRefusal("LOCAL_LIFECYCLE_LAST_ACTION_INVALID")
    if not isinstance(value.get("root_hash"), str) or not value["root_hash"]:
        raise LifecycleRefusal("LOCAL_LIFECYCLE_ROOT_BINDING_MISSING")
    return value


def _write_local_state(state_root, root_hash: str, state: Mapping[str, Any]) -> None:
    path = local_state_path(state_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "root_hash": root_hash,
        "mode": state["mode"],
        "sequence": state["sequence"],
        "last_action": state["last_action"],
        "local_only": True,
        "world_event_created": False,
        "clock_changed": False,
        "simulated_delivery": False,
    }
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf8")
    os.replace(temporary, path)


def _local_result(
    *,
    control: str,
    status: str,
    code: str,
    reason: str,
    refusal: bool,
    mode: str,
    state: Mapping[str, Any],
    surface: list[str] | None = None,
) -> dict:
    return {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "source": "s45",
        "control": control,
        "status": status,
        "code": code,
        "reason": reason,
        "attempted": True,
        "performed": False,
        "world_event_created": False,
        "clock_changed": False,
        "actor_response_generated": False,
        "simulated_delivery": False,
        "refusal": refusal,
        "mode": mode,
        "local_only": True,
        "user_attempt": {
            "control": control,
            "input": "",
            "accepted": None,
            "attempted": True,
            "performed": False,
        },
        "actor_response": None,
        "event_ids": [],
        "surface": list(surface or []),
        "lifecycle": _public_state(state),
    }


class LifecycleEncounter:
    """One S45 projection with persistent local portal/outside mode."""

    def __init__(self, projection, state_root, root_hash: str, local_state: dict | None) -> None:
        self.projection = projection
        self.state_root = Path(state_root)
        self.root_hash = root_hash
        self._state = dict(local_state or _default_state())
        self.projection.mode = self._state["mode"]

    @classmethod
    def _wrap(cls, projection, state_root) -> "LifecycleEncounter":
        root_hash = projection.session.read_root()["root_hash"]
        try:
            local = _load_local_state(state_root)
            if local is not None and local["root_hash"] != root_hash:
                raise LifecycleRefusal(
                    "LOCAL_LIFECYCLE_ROOT_MISMATCH",
                    "local mode is bound to a different root",
                )
            return cls(projection, state_root, root_hash, local)
        except Exception:
            projection.close()
            raise

    @classmethod
    def start(cls, state_root, *, seed: str = "01" * 32, **kwargs) -> "LifecycleEncounter":
        projection = runtime.projection_class().start(state_root, seed=seed, **kwargs)
        return cls._wrap(projection, state_root)

    @classmethod
    def open(cls, state_root, **kwargs) -> "LifecycleEncounter":
        projection = runtime.projection_class().open(state_root, **kwargs)
        return cls._wrap(projection, state_root)

    @property
    def mode(self) -> str:
        return self._state["mode"]

    @property
    def local_state_path(self) -> Path:
        return local_state_path(self.state_root)

    def local_state(self) -> dict:
        return _public_state(self._state)

    def view(self) -> dict:
        return self.projection.view()

    def status(self) -> dict:
        return self.projection.status()

    def _blocked(self, control: str) -> dict:
        return _local_result(
            control=control,
            status="REFUSED",
            code=BLOCKED_CODE,
            reason="LOCAL_OUTSIDE_MODE_NO_ENCOUNTER_ACTION",
            refusal=True,
            mode="OUTSIDE",
            state=self._state,
            surface=["Local encounter is closed; return locally to continue."],
        )

    def say(self, text: str) -> dict:
        if self.mode != "PORTAL":
            return self._blocked("SAY")
        return self.projection.say(text)

    def do_help(self) -> dict:
        if self.mode != "PORTAL":
            return self._blocked("DO_HELP")
        return self.projection.do_help()

    def attend(self) -> dict:
        if self.mode != "PORTAL":
            return self._blocked("ATTEND")
        return self.projection.attend()

    def exit(self) -> dict:
        if self.mode == "OUTSIDE":
            return self.projection.exit()
        result = self.projection.exit()
        self._state.update(
            mode="OUTSIDE",
            sequence=self._state["sequence"] + 1,
            last_action="LOCAL_EXIT",
        )
        self.projection.mode = "OUTSIDE"
        _write_local_state(self.state_root, self.root_hash, self._state)
        return result

    def return_(self) -> dict:
        if self.mode == "PORTAL":
            return self.projection.return_()
        self._state.update(
            mode="PORTAL",
            sequence=self._state["sequence"] + 1,
            last_action="LOCAL_RETURN",
        )
        self.projection.mode = "PORTAL"
        _write_local_state(self.state_root, self.root_hash, self._state)
        return _local_result(
            control="RETURN",
            status="OK",
            code=RETURN_CODE,
            reason="LOCAL_UI_MODE_RETURN_NO_WORLD_SIMULATION",
            refusal=False,
            mode="PORTAL",
            state=self._state,
            surface=["Local encounter reopened; no world time or activity simulated."],
        )

    def close(self) -> None:
        self.projection.close()


__all__ = [
    "BLOCKED_CODE",
    "GRADE",
    "LifecycleEncounter",
    "LifecycleRefusal",
    "MODES",
    "RESULT_SCHEMA",
    "RETURN_CODE",
    "SCHEMA",
    "local_state_path",
]
