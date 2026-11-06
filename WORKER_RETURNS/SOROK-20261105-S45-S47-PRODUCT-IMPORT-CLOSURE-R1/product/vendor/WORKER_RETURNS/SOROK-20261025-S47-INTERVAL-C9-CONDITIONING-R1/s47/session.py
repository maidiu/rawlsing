"""S47 interval-to-C9 conditioning over the actual S46 person."""
from __future__ import annotations

from .bootstrap import install

install()

from s42.bindings import binding_episodes  # noqa: E402
from s42.reader import S42ReadRefusal  # noqa: E402
import s42.reader as s42_reader  # noqa: E402
from s46.session import S46Session  # noqa: E402
import s41.reader as s41_reader  # noqa: E402

from .conditioning import (  # noqa: E402
    current_interval_source,
    qualify_source,
    validate_event_source,
)

S47_SCHEMA = "SOROK_S47_INTERVAL_C9_CONDITIONING_SESSION@1"


class S47Session(S46Session):
    """S46 person whose S46 interval source participates in real C9."""

    def _extra_conditioning_sources(self) -> list[dict]:
        source = current_interval_source(self)
        return [qualify_source(self, source)] if source else []

    def c9_interval_source(self) -> dict | None:
        return current_interval_source(self)

    def read_c9_conditioning(self, event_ref: str | None = None) -> dict:
        bindings = binding_episodes(self)
        if event_ref is None:
            if not bindings:
                raise LookupError("S47_C9_BINDING_MISSING")
            selected = bindings[-1]["e1_event_id"]
        else:
            if not isinstance(event_ref, str) or not event_ref.strip():
                raise S42ReadRefusal("S42_EVENT_NOT_FOUND")
            selected = event_ref
        all_bindings = self._all_bindings()
        binding = s42_reader._find_binding(all_bindings, selected)
        if binding is None:
            raise S42ReadRefusal("S42_EVENT_NOT_FOUND")
        event_read = s42_reader.read_event(self, selected)
        c9_binding = binding.get("c9")
        if not isinstance(c9_binding, dict):
            raise S42ReadRefusal("S42_C9_BINDING_MISSING")
        response, receipt, _ = s41_reader._read_c9(c9_binding)
        if response.get("event_ref") != binding.get("e1_event_hash"):
            raise S42ReadRefusal("S42_C9_RESPONSE_EVENT_MISMATCH")
        if receipt.get("response_ref") != c9_binding.get("response_ref"):
            raise S42ReadRefusal("S42_C9_RECEIPT_RESPONSE_MISMATCH")
        s35 = response.get("s35_receipt") or {}
        readset = list(s35.get("readset_refs") or [])
        source_refs = [
            ref for ref in readset
            if isinstance(ref, str)
            and ref.startswith("TEST_ONLY_S47_INTERVAL_")
        ]
        if len(set(source_refs)) > 1:
            raise S47Refusal("S47_SOURCE_READSET_AMBIGUOUS")
        if source_refs:
            s36 = binding.get("s36")
            if not isinstance(s36, dict):
                raise S47Refusal("S47_EVENT_SOURCE_BINDING_MISSING")
            if s36.get("e1_event_hash") != event_read.get("e1_event_hash"):
                raise S47Refusal("S47_EVENT_SOURCE_EVENT_MISMATCH")
            candidates = [
                row for row in s36.get("conditioning_sources") or []
                if isinstance(row, dict)
                and row.get("source_ref") == source_refs[0]
            ]
            if len(candidates) != 1:
                raise S47Refusal("S47_EVENT_SOURCE_BINDING_MISSING")
            historical_source = validate_event_source(
                candidates[0],
                expected_ref=source_refs[0],
                actor_id=event_read.get("actor_id"),
                branch_id=event_read.get("branch_id"),
                event_time=event_read.get("event_time"),
            )
        else:
            historical_source = None
        current_source = current_interval_source(self)
        current_states = [
            row for row in self.read_interval_states()
            if row.get("currentness") == "CURRENT"
        ]
        present = current_states[-1] if current_states else None
        present_revoked = bool(
            present and self._condition_revoked(present["state_id"])
        )
        historical_revoked = bool(
            historical_source
            and self._condition_revoked(
                historical_source["content"]["interval_state_id"]
            )
        )
        return {
            "schema": "SOROK_S47_C9_CONDITIONING_READ@1",
            "event_ref": event_read.get("e1_event_hash"),
            "selected_event_ref": selected,
            "response_status": response.get("status"),
            "readset_refs": readset,
            "s47_source_ref": (
                historical_source.get("source_ref") if historical_source else ""
            ),
            "s47_source_hash": (
                historical_source.get("source_hash") if historical_source else ""
            ),
            "s47_source_currentness": (
                (historical_source.get("content") or {}).get("currentness")
                if historical_source else ""
            ),
            "s47_source_coverage": (
                (historical_source.get("content") or {}).get("coverage")
                if historical_source else []
            ),
            "s47_source_in_readset": bool(
                historical_source
                and historical_source.get("source_ref") in readset
            ),
            "historical_source": historical_source,
            "current_source": current_source,
            "current_source_ref": (
                current_source.get("source_ref") if current_source else ""
            ),
            "current_source_hash": (
                current_source.get("source_hash") if current_source else ""
            ),
            "present_interval_state_id": (
                present.get("state_id") if present else ""
            ),
            "present_interval_currentness": (
                present.get("currentness") if present else "ABSENT"
            ),
            "present_condition_revoked": present_revoked,
            "historical_condition_revoked": historical_revoked,
            "objective_material_eligible": s35.get("objective_material_eligible"),
            "objective_material_refs": list(s35.get("objective_material_refs") or []),
            "target_branch": receipt.get("target_branch"),
            "target_reason": receipt.get("target_reason"),
            "target_proposals": list(s35.get("target_proposals") or []),
            "historical_source_ref": (
                historical_source.get("source_ref") if historical_source else ""
            ),
            "s47_source": historical_source,
        }

    def verify(self) -> dict:
        result = super().verify()
        try:
            source = current_interval_source(self)
            result["s47_conditioning"] = {
                "status": "OK" if source else "NO_CURRENT_INTERVAL",
                "source_ref": source.get("source_ref") if source else "",
                "source_class": source.get("source_class") if source else "",
            }
            ok = True
        except Exception as exc:
            result["s47_conditioning"] = {
                "status": "REFUSED", "code": getattr(exc, "code", type(exc).__name__),
            }
            ok = False
        result["ok"] = bool(result.get("ok")) and ok
        return result


__all__ = ["S47_SCHEMA", "S47Session"]
