"""Explicit adapter from a pinned S45 session to the WP19 encounter surface."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .contract import CONTRACT_SCHEMA
from .runtime import install_package_closure
from .projection import (
    GRADE,
    RESULT_SCHEMA,
    SOURCE,
    STATUS_SCHEMA,
    TYPED_HOLDS,
    VIEW_SCHEMA,
    project_result,
    project_view,
)


def _store_hash(path: Path) -> str:
    if not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class S45Projection:
    """One S45 session projected through the pinned WP19 surface."""

    def __init__(self, session) -> None:
        self.session = session
        self.mode = "PORTAL"
        self._last_result: dict | None = None
        self._last_source_result: dict | None = None
        self._baseline_store_hash = self._current_store_hash()

    @classmethod
    def open(cls, state_root, **kwargs) -> "S45Projection":
        install_package_closure()
        from s45.session import S45Session

        return cls(S45Session.open(state_root, **kwargs))

    @classmethod
    def start(
        cls,
        state_root,
        *,
        seed: str = "01" * 32,
        bundle=None,
        case=None,
        source=None,
        language_context=None,
        attention: str = "focused",
        **kwargs,
    ) -> "S45Projection":
        install_package_closure()
        from s45.fixtures import root_bundle
        from s45.session import S45Session
        from s37.harness import case_for, source_for

        selected_case = case if case is not None else case_for(True)
        selected_source = (
            source if source is not None else source_for(selected_case)
        )
        selected_bundle = (
            bundle if bundle is not None else root_bundle(seed)
        )
        session = S45Session.start(
            state_root,
            bundle=selected_bundle,
            case=selected_case,
            source=selected_source,
            language_context=language_context,
            attention=attention,
            **kwargs,
        )
        return cls(session)

    @property
    def last_source_result(self) -> dict | None:
        return dict(self._last_source_result) if self._last_source_result else None

    def _store_path(self) -> Path:
        return Path(self.session.product.store.path)

    def _current_store_hash(self) -> str:
        return _store_hash(self._store_path())

    def _capture(self, result: dict) -> None:
        self._last_source_result = dict(result)

    def _base_result(
        self,
        *,
        status: str,
        code: str,
        reason: str = "",
        attempted: bool = True,
        clock_changed: bool = False,
        world_event_created: bool = False,
        store_hash_before: str = "",
        store_hash_after: str = "",
        **extra: Any,
    ) -> dict:
        return {
            "schema": RESULT_SCHEMA,
            "grade": GRADE,
            "native": False,
            "source": SOURCE,
            "control": extra.pop("control", code),
            "status": status,
            "code": code,
            "reason": reason,
            "attempted": attempted,
            "performed": False,
            "world_event_created": world_event_created,
            "clock_changed": clock_changed,
            "actor_response_generated": False,
            "simulated_delivery": False,
            "refusal": False,
            "mode": self.mode,
            "user_attempt": None,
            "actor_response": None,
            "event_ids": [],
            "surface": [],
            "store_hash_before": store_hash_before,
            "store_hash_after": store_hash_after,
            **extra,
        }

    def view(self) -> dict:
        return project_view(self.session, mode=self.mode)

    def say(self, text: str) -> dict:
        before_hash = self._current_store_hash()
        before_clock = self.session.clock()
        source_result = self.session.say(text)
        self._capture(source_result)
        after_clock = self.session.clock()
        after_hash = self._current_store_hash()
        result = project_result(
            "SAY",
            source_result,
            user_input=text,
            clock_before=before_clock,
            clock_after=after_clock,
            store_hash_before=before_hash,
            store_hash_after=after_hash,
            mode=self.mode,
        )
        self._last_result = result
        return result

    def do_help(self) -> dict:
        before_hash = self._current_store_hash()
        before_clock = self.session.clock()
        source_result = self.session.do_help()
        self._capture(source_result)
        after_clock = self.session.clock()
        after_hash = self._current_store_hash()
        result = project_result(
            "DO_HELP",
            source_result,
            user_input="help",
            clock_before=before_clock,
            clock_after=after_clock,
            store_hash_before=before_hash,
            store_hash_after=after_hash,
            mode=self.mode,
        )
        self._last_result = result
        return result

    def attend(self) -> dict:
        before_hash = self._current_store_hash()
        before_clock = self.session.clock()
        source_result = self.session.attend()
        self._capture(source_result)
        after_clock = self.session.clock()
        after_hash = self._current_store_hash()
        result = project_result(
            "ATTEND",
            source_result,
            user_input="attend",
            clock_before=before_clock,
            clock_after=after_clock,
            store_hash_before=before_hash,
            store_hash_after=after_hash,
            mode=self.mode,
        )
        self._last_result = result
        return result

    def wait(self) -> dict:
        before_hash = self._current_store_hash()
        result = self._base_result(
            control="WAIT",
            status="HELD",
            code=TYPED_HOLDS["WAIT"],
            reason=TYPED_HOLDS["WAIT"],
            store_hash_before=before_hash,
            store_hash_after=before_hash,
        )
        self._last_result = result
        return result

    def exit(self) -> dict:
        before_hash = self._current_store_hash()
        self.mode = "OUTSIDE"
        result = self._base_result(
            control="EXIT",
            status="OK",
            code=TYPED_HOLDS["EXIT"],
            reason="LOCAL_UI_EXIT_ONLY_NO_ACTOR_OR_WORLD_EVENT",
            store_hash_before=before_hash,
            store_hash_after=before_hash,
        )
        self._last_result = result
        return result

    def return_(self) -> dict:
        before_hash = self._current_store_hash()
        result = self._base_result(
            control="RETURN",
            status="HELD",
            code=TYPED_HOLDS["RETURN"],
            reason=TYPED_HOLDS["RETURN"],
            store_hash_before=before_hash,
            store_hash_after=before_hash,
        )
        self._last_result = result
        return result

    def absence(self) -> dict:
        before_hash = self._current_store_hash()
        result = self._base_result(
            control="ABSENCE",
            status="UNKNOWN",
            code=TYPED_HOLDS["ABSENCE"],
            reason="ABSENCE_NOT_SIMULATED",
            store_hash_before=before_hash,
            store_hash_after=before_hash,
        )
        self._last_result = result
        return result

    def status(self) -> dict:
        current = self._current_store_hash()
        return {
            "schema": STATUS_SCHEMA,
            "grade": GRADE,
            "native": False,
            "source": SOURCE,
            "projection_contract": CONTRACT_SCHEMA,
            "mode": self.mode,
            "root": str(Path(self.session.state_root)),
            "store_path": str(self._store_path()),
            "baseline_store_hash": self._baseline_store_hash,
            "current_store_hash": current,
            "store_mutated_since_load": current != self._baseline_store_hash,
            "last_result": self._last_result,
        }

    def close(self) -> None:
        self.session.close()


__all__ = ["S45Projection"]
