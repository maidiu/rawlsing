"""C12/C8-bound provenance for the persisted J source.

The J product persists a sidecar and the session persists metadata. Neither is
authoritative by itself. This module compares both with the C12 ``GM01_SOURCE``
episode and the keyed C8 occurrence, and checks the source/actor map plus the
C8/E1/target receipt fields.
"""
from __future__ import annotations

from .b_event import persisted_binding, validate_binding


def _c8_source(product) -> tuple[dict, dict]:
    from c8_readonly_consumer import C8ReadOnlyConsumer

    view = C8ReadOnlyConsumer(str(product.artifacts.journal_path)).load()
    event = view.get(product.artifacts.occurrence_id)
    if not event:
        raise ValueError("C8_OCCURRENCE_ABSENT")
    source = (event.get("payload") or {}).get("gm01_pre_c9_source")
    if not isinstance(source, dict):
        raise ValueError("C8_GM01_SOURCE_ABSENT")
    return source, event


def _c12_source(product, branch_id: str) -> tuple[dict, dict]:
    rows = [row for row in product.store.episodes(branch_id)
            if row["kind"] == "GM01_SOURCE"]
    if len(rows) != 1:
        raise ValueError("C12_GM01_SOURCE_COUNT:" + str(len(rows)))
    row = rows[0]
    source = (row.get("body") or {}).get("gm01_source")
    if not isinstance(source, dict):
        raise ValueError("C12_GM01_SOURCE_ABSENT")
    return source, row


def validate_join(product, meta: dict, branch_id: str) -> dict:
    """Return a check map; callers turn a false result into a typed refusal."""
    checks: dict[str, bool] = {}
    observed: dict = {}
    try:
        c8_source, c8_event = _c8_source(product)
        c12_source, c12_row = _c12_source(product, branch_id)
        artifact = product.artifacts
        custody = product.joined_source()["custody"]
        seed = product.seed.public()
        source = product.source
        expected_map = {
            "TEST_ONLY_R31J_A": seed["actor_a"],
            "TEST_ONLY_R31J_B": seed["actor_b"],
        }
        payload = c8_event.get("payload") or {}
        actor = payload.get("actor") or {}
        other = payload.get("other_actor") or {}
        body = c12_row.get("body") or {}
        persisted = persisted_binding(product, branch_id)
        binding_check = validate_binding(meta, persisted, source)
        checks.update({
            "b_event_binding_ok": binding_check.get("ok") is True,
            "sidecar_matches_c8": source == c8_source,
            "sidecar_matches_c12": source == c12_source,
            "meta_matches_c8": meta.get("j_source") == c8_source,
            "meta_matches_c12": meta.get("j_source") == c12_source,
            "c8_actor_is_seed_a": actor.get("actor_id") == seed.get("actor_a"),
            "c8_other_is_seed_b": other.get("actor_id") == seed.get("actor_b"),
            "source_actor_map": meta.get("source_actor_map") == expected_map,
            "source_b_is_seed_b": source.get("b_actor") == "TEST_ONLY_R31J_B",
            "source_b_to_is_seed_a": source.get("b_to_actor") == "TEST_ONLY_R31J_A",
            "meta_target_matches_artifact": meta.get("j_target_id") == artifact.target_id,
            "meta_c8_matches_artifact": meta.get("j_c8_state_digest") == artifact.c8_state_digest,
            "meta_e1_matches_artifact": meta.get("j_e1_event_hash") == artifact.e1_event_hash,
            "c12_target_matches_artifact": body.get("c9_target_id") == artifact.target_id,
            "c12_c8_matches_artifact": body.get("c8_state_digest") == artifact.c8_state_digest,
            "c12_e1_matches_artifact": body.get("e1_event_hash") == artifact.e1_event_hash,
            "custody_target_matches_artifact": custody.get("target_id") == artifact.target_id,
            "custody_c8_matches_artifact": custody.get("c8_state_digest") == artifact.c8_state_digest,
            "custody_e1_matches_artifact": custody.get("e1_event_hash") == artifact.e1_event_hash,
        })
        try:
            product.verify_join()
            checks["joined_source_verifies"] = True
        except Exception as exc:  # typed source refusal becomes a failed check
            checks["joined_source_verifies"] = False
            observed["verify_join_error"] = type(exc).__name__ + ":" + str(exc)
        if binding_check.get("required"):
            observed["b_event_binding"] = binding_check.get("observed", {})
        observed.update({
            "b_event_hash": source.get("b_event_hash"),
            "b_operation": source.get("b_operation"),
            "b_actor": source.get("b_actor"),
            "b_to_actor": source.get("b_to_actor"),
            "c8_state_digest": artifact.c8_state_digest,
            "e1_event_hash": artifact.e1_event_hash,
            "target_id": artifact.target_id,
            "source_actor_map": meta.get("source_actor_map"),
            "seed_actors": {"a": seed.get("actor_a"), "b": seed.get("actor_b")},
        })
    except Exception as exc:  # missing/orphan source is a failed provenance check
        checks["provenance_readable"] = False
        observed["error"] = type(exc).__name__ + ":" + str(exc)
    checks.setdefault("provenance_readable", True)
    return {"ok": all(checks.values()), "checks": checks, "observed": observed}
