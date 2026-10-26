"""S50 recovered V3 projection over the same S49 canonical person."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import digest  # noqa: E402
from s49.session import S49Session  # noqa: E402

from .recovery import MISSING_ACTUAL, RECOVERED_GRADE, run_legacy_fixture, verify_source

S50_SCHEMA = "SOROK_S50_HISTORICAL_V3_ACTOR_RECOVERY@1"
PROJECTION_KIND = "S50_HISTORICAL_V3_PROJECTION"


class S50Session(S49Session):
    """Accepted S49 person plus read-only recovered V3 projection evidence."""

    def materialize_legacy_projection(self, *, years: int = 1) -> dict:
        identity = verify_source()
        if not identity.get("all_exact"):
            raise RuntimeError("S50_SOURCE_IDENTITY_MISMATCH")
        run = run_legacy_fixture(years=years)
        projection = run["projection"]
        body = {
            "schema": S50_SCHEMA,
            "stage": "HISTORICAL_V3_PROJECTION",
            "grade": RECOVERED_GRADE,
            "native": False,
            "psychology_claim": False,
            "fixture_only": True,
            "actual_person_commit": False,
            "read_only": True,
            "second_mind": False,
            "canonical_parents": {
                "root_hash": self.read_root().get("root_hash"),
                "root_id": self.read_root().get("root_id"),
                "actor_id": (self.world().actor_state.get("A") or {}).get("actor_id"),
                "actor_role": "A",
                "branch_id": self.branch_id,
                "store": str(self.state_root),
            },
            "source_identity": run["source_identity"],
            "run_hash": digest(run),
            "projection": projection,
            "state_json": None,
            "missing_actual_fields": self.actual_root_missing()["missing_fields"],
        }
        episode = self._append(PROJECTION_KIND, body)
        return {
            "schema": S50_SCHEMA,
            "status": "LEGACY_PROJECTION_MATERIALIZED",
            "episode_id": episode["episode_id"],
            "run_hash": body["run_hash"],
            "projection_hash": projection["state_sha256"],
            "fixture_sha256": run["fixture_sha256"],
            "actual_person_commit": False,
            "source_all_exact": run["source_identity"]["all_exact"],
            "missing_actual_fields": body["missing_actual_fields"],
        }

    def read_projection(self) -> dict | None:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") == PROJECTION_KIND
        ]
        return dict(rows[-1].get("body") or {}) if rows else None

    def actual_root_missing(self) -> dict:
        root = self.read_root()
        state = (self.world().actor_state.get("B") or {})
        missing = [
            field for field in (
                "backbone_state", "initial_state_provenance",
                "expectation_baseline", "striving_objects",
                "pressure_flow_history", "pressure_flow_memory",
                "surface_psyche_profile", "analyst_pressure_account",
                "actor_context_projection", "actor_owned_source",
            )
            if field not in state
        ]
        return {
            "schema": "S50_ACTUAL_ROOT_STATE_COMPARISON@1",
            "status": "SOURCE_OWNER_HOLD",
            "reason": MISSING_ACTUAL,
            "canonical_parents": {
                "root_hash": root.get("root_hash"),
                "root_id": root.get("root_id"),
                "branch_id": self.branch_id,
                "b_actor_id": state.get("actor_id"),
                "b_position": (self.world().positions or {}).get("B"),
            },
            "missing_fields": missing,
            "actual_commit": False,
            "no_default_seed": True,
            "native": False,
            "psychology_claim": False,
        }

    def verify(self) -> dict:
        result = super().verify()
        try:
            projection = self.read_projection()
            result["s50_historical_v3"] = {
                "status": "OK" if projection else "NO_PROJECTION",
                "grade": RECOVERED_GRADE,
                "read_only": True,
                "second_mind": False,
                "actual_person_commit": False,
                "source_all_exact": (
                    (projection or {}).get("source_identity", {}).get("all_exact")
                    if projection else False
                ),
                "missing_actual_fields": (
                    (projection or {}).get("missing_actual_fields", [])
                    if projection else []
                ),
            }
            ok = True
        except Exception as exc:
            result["s50_historical_v3"] = {
                "status": "REFUSED", "code": getattr(exc, "code", type(exc).__name__),
            }
            ok = False
        result["ok"] = bool(result.get("ok")) and ok
        return result


__all__ = ["PROJECTION_KIND", "S50_SCHEMA", "S50Session"]
