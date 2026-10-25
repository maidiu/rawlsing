"""S47 interval-to-C9 conditioning over the actual S46 person."""
from __future__ import annotations

from .bootstrap import install

install()

from s42.bindings import binding_episodes  # noqa: E402
from s46.session import S46Session  # noqa: E402
import s41.reader as s41_reader  # noqa: E402

from .conditioning import current_interval_source, qualify_source  # noqa: E402

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
        if not bindings:
            raise LookupError("S47_C9_BINDING_MISSING")
        binding = bindings[-1]
        response, receipt, _ = s41_reader._read_c9(binding["c9"])
        s35 = response.get("s35_receipt") or {}
        source = current_interval_source(self)
        return {
            "schema": "SOROK_S47_C9_CONDITIONING_READ@1",
            "event_ref": response.get("event_ref"),
            "response_status": response.get("status"),
            "readset_refs": list(s35.get("readset_refs") or []),
            "s47_source_ref": source.get("source_ref") if source else "",
            "s47_source_hash": source.get("source_hash") if source else "",
            "s47_source_currentness": (
                (source.get("content") or {}).get("currentness") if source else ""
            ),
            "s47_source_coverage": (
                (source.get("content") or {}).get("coverage") if source else []
            ),
            "s47_source_in_readset": bool(
                source and source.get("source_ref") in (s35.get("readset_refs") or [])
            ),
            "objective_material_eligible": s35.get("objective_material_eligible"),
            "objective_material_refs": list(s35.get("objective_material_refs") or []),
            "target_branch": receipt.get("target_branch"),
            "target_reason": receipt.get("target_reason"),
            "target_proposals": list(s35.get("target_proposals") or []),
            "s47_source": source,
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
