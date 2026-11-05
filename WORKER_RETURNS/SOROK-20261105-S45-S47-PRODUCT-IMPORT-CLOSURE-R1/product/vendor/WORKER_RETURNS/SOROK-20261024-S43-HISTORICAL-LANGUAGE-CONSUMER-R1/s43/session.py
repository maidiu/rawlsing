"""S43 ongoing person adapter: historical repertoire before generated speech."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

import s42.session as s42_session  # noqa: E402
from s42.session import S42Session  # noqa: E402

from .performer import perform_historical_attempt  # noqa: E402
from .reader import S43ReadRefusal, read_s43_event  # noqa: E402
from .registry import ATOMS, PAIRS  # noqa: E402

S43_SCHEMA = "SOROK_S43_HISTORICAL_LANGUAGE_SESSION@1"


class S43Session(S42Session):
    """Same S42 person with S43 source-bound speaking for later events."""

    @classmethod
    def start(cls, state_root, *, language_context: Mapping[str, Any] | None = None,
              **kwargs) -> "S43Session":
        session = super().start(state_root, **kwargs)
        session._s43_active_context = None
        session.meta["s43_schema"] = S43_SCHEMA
        if language_context is not None:
            session.meta["s43_language_context"] = dict(language_context)
        session._save_join_meta()
        return session

    def s43_context(self) -> dict | None:
        active = getattr(self, "_s43_active_context", None)
        if active is not None:
            return dict(active)
        value = self.meta.get("s43_language_context")
        return dict(value) if isinstance(value, Mapping) else None

    def set_language_context(self, context: Mapping[str, Any]) -> None:
        if not isinstance(context, Mapping) or not context.get("milieu_id"):
            raise S43ReadRefusal("S43_EXPRESSION_CONTEXT_REQUIRED")
        self.meta["s43_language_context"] = dict(context)
        self._save_join_meta()

    def _perform_attempt(self, session, attempt_request, *,
                         generation_receipt, e1_identity):
        return perform_historical_attempt(
            session,
            attempt_request,
            generation_receipt=generation_receipt,
            e1_identity=e1_identity,
        )

    def admit_event(self, *, language_context: Mapping[str, Any] | None = None,
                    **kwargs) -> dict:
        previous = getattr(self, "_s43_active_context", None)
        if language_context is not None:
            self._s43_active_context = dict(language_context)
        else:
            self._s43_active_context = None
        original = s42_session.perform_continuation_attempt
        s42_session.perform_continuation_attempt = self._perform_attempt
        try:
            return super().admit_event(**kwargs)
        finally:
            s42_session.perform_continuation_attempt = original
            self._s43_active_context = previous

    def _projection_verification(self, event, lme, projection):
        import s40.session as s40_session

        original_pairs, original_atoms = s40_session.S40_PAIRS, s40_session.S40_ATOMS
        s40_session.S40_PAIRS, s40_session.S40_ATOMS = PAIRS, ATOMS
        try:
            return super()._projection_verification(event, lme, projection)
        finally:
            s40_session.S40_PAIRS = original_pairs
            s40_session.S40_ATOMS = original_atoms

    def read_s43_event(self, event_ref: str) -> dict:
        return read_s43_event(self, event_ref)

    def read_s43_events(self) -> list[dict]:
        return [self.read_s43_event(row["e1_event_id"])
                for row in self.read_events()]

    def verify(self) -> dict:
        result = super().verify()
        summaries = []
        s43_ok = True
        try:
            for row in self.read_events():
                if row.get("event_ordinal") == 1:
                    continue
                if not row.get("performed") or row.get("action_event_kind") != "SPEECH":
                    continue
                read = self.read_s43_event(row["e1_event_id"])
                s43 = read.get("s43") or {}
                summaries.append({
                    "event_ordinal": row["event_ordinal"],
                    "repertoire_id": s43.get("repertoire_id", ""),
                    "repertoire_hash": s43.get("repertoire_hash", ""),
                    "selected_relation_ids": s43.get("selected_relation_ids", []),
                    "contrary_relation_ids": s43.get("contrary_relation_ids", []),
                    "currently_available": s43.get("currently_available", False),
                })
        except (S43ReadRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
            s43_ok = False
        result["s43_events"] = summaries
        result["ok"] = bool(result.get("ok")) and s43_ok
        return result

    def status(self) -> dict:
        result = super().status()
        summaries = []
        try:
            for row in self.read_events():
                if row.get("event_ordinal") == 1:
                    continue
                if not row.get("performed") or row.get("action_event_kind") != "SPEECH":
                    continue
                read = self.read_s43_event(row["e1_event_id"])
                s43 = read.get("s43") or {}
                summaries.append({
                    "event_ordinal": row["event_ordinal"],
                    "repertoire_id": s43.get("repertoire_id", ""),
                    "repertoire_hash": s43.get("repertoire_hash", ""),
                    "native_text": (read.get("language") or {}).get("native_text", ""),
                    "selected_relation_ids": s43.get("selected_relation_ids", []),
                    "currently_available": s43.get("currently_available", False),
                })
        except (S43ReadRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
        result.update({
            "schema": S43_SCHEMA,
            "s43_events": summaries,
            "s43_language_context": self.s43_context(),
        })
        return result


__all__ = ["S43_SCHEMA", "S43Session"]
