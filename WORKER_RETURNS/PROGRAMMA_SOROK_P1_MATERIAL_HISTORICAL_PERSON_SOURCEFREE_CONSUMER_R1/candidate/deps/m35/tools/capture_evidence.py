"""Capture the sourcefree first-class B chain evidence as JSON."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RETURN))
import install  # noqa: E402

install.install()

import bp2_joined  # noqa: E402
import firstclass  # noqa: E402
from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from joined.refusal import RefusalSession  # noqa: E402
from joined.session import JoinedSession  # noqa: E402
from r31j.scenarios import evaluated  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _share_c8(session):
    artifacts = session.product.artifacts
    view = C8ReadOnlyConsumer(str(artifacts.journal_path)).load()
    event = view.get(artifacts.occurrence_id) or {}
    payload = event.get("payload") or {}
    return {
        "occurrence_id": artifacts.occurrence_id,
        "journal_path": str(artifacts.journal_path),
        "state_digest": session.meta["j_c8_state_digest"],
        "source": payload.get("gm01_pre_c9_source"),
        "source_matches_product": payload.get("gm01_pre_c9_source") == session.product.source,
        "material_ref": (payload.get("world") or {}).get("material_ref"),
        "material_receipt_id": (payload.get("world") or {}).get("material_receipt_id"),
    }


def _refusal_c8(session):
    binding = session.product.c8_binding
    view = C8ReadOnlyConsumer(str(binding["journal_path"])).load()
    event = view.get(binding["occurrence_id"]) or {}
    payload = event.get("payload") or {}
    return {
        "occurrence_id": binding["occurrence_id"],
        "journal_path": binding["journal_path"],
        "state_digest": binding["c8_state_digest"],
        "source": payload.get("gm01_pre_c9_source"),
        "source_matches_product": payload.get("gm01_pre_c9_source") == session.product.source,
        "material_ref": (payload.get("world") or {}).get("material_ref"),
        "material_receipt_id": (payload.get("world") or {}).get("material_receipt_id"),
    }


def _material_inspects(session):
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == "DO"
        and (row.get("body") or {}).get("action") == "material_inspect"
        and (row.get("body") or {}).get("admitted") is True
    ]


def _tools(session):
    return session.product._world(session.branch_id).actor_state["A"]["tools_remaining"]


with tempfile.TemporaryDirectory(prefix="m35-firstclass-") as temporary:
    root = Path(temporary)
    share = JoinedSession.start(root / "share", perform="omit")
    try:
        share_help = share.do_help()
        share_record = {
            "source": share.product.source,
            "c8": _share_c8(share),
            "target_id": share.meta["j_target_id"],
            "tools_remaining": _tools(share),
            "e_do_help": {
                "accepted": share_help["accepted"],
                "strategy": share_help["strategy"],
            },
            "admitted_material_inspects": len(_material_inspects(share)),
        }
    finally:
        share.close()
    cold_share = JoinedSession.open(root / "share")
    try:
        share_record["cold_reopen_verify"] = cold_share.verify()["ok"]
    finally:
        cold_share.close()

    refusal = RefusalSession.start(root / "refuse")
    try:
        refusal_help = refusal.do_help()
        refusal_record = {
            "source": refusal.product.source,
            "c8": _refusal_c8(refusal),
            "c9": refusal.meta["c9"],
            "target_id": refusal.meta["target_id"],
            "targetless": refusal.meta["targetless"],
            "tools_remaining": _tools(refusal),
            "e_do_help": {
                "accepted": refusal_help["accepted"],
                "strategy": refusal_help["strategy"],
            },
            "admitted_material_inspects": len(_material_inspects(refusal)),
            "cold_reopen_verify": None,
        }
    finally:
        refusal.close()
    cold_refusal = RefusalSession.open(root / "refuse")
    try:
        refusal_record["cold_reopen_verify"] = cold_refusal.verify()["ok"]
    finally:
        cold_refusal.close()

    e2 = JoinedSession.start(root / "e2", perform="e2")
    try:
        e2_help = e2.do_help()
        e2_record = {
            "source_operation": e2.product.source["b_operation"],
            "source_performed": e2.product.source["b_performed"],
            "tools_remaining": _tools(e2),
            "admitted_material_inspects": len(_material_inspects(e2)),
            "e_do_help": {
                "accepted": e2_help["accepted"],
                "strategy": e2_help["strategy"],
            },
        }
    finally:
        e2.close()

    restored = JoinedSession.start(root / "restored", perform="omit")
    try:
        restored_record = {
            "source_operation": restored.product.source["b_operation"],
            "e_do_help": restored.do_help(),
            "admitted_material_inspects": len(_material_inspects(restored)),
        }
    finally:
        restored.close()

    derived, producer = firstclass.c9_only(
        root / "derived", gm01={"material_feasible_after": False},
        case=evaluated(share=True, e2=False)["case"])
    try:
        derived_record = {
            "gm01_boolean_supplied": False,
            "source_operation": derived["gm01_source"]["b_operation"],
            "material_access": derived["material_access"],
            "tools_remaining": producer.historical_life.a_snapshot["state"]["tools_remaining"],
            "c9_target_branch": derived["c9"]["target_branch"],
            "c9_target_id": derived["c9"]["target_id"],
        }
    finally:
        producer.close()

    result = {
        "schema": "M35_FIRSTCLASS_B_EVIDENCE@1",
        "grade": "TEST_ONLY_SOURCEFREE",
        "loaded": {
            "bp2_joined": str(Path(bp2_joined.__file__).resolve()),
            "material_source": str(Path(bp2_joined.material_source.__file__).resolve()),
            "same_producer": firstclass.JoinedProducer is bp2_joined.JoinedProducer,
            "vendor_file_count": bp2_joined.verify_sources()["file_count"],
            "bp2_vendor": str(bp2_joined.bootstrap.VENDOR),
            "source_manifest_sha256": _sha(bp2_joined.bootstrap.MANIFEST),
        },
        "share": share_record,
        "refusal": refusal_record,
        "share_e2": e2_record,
        "restored_share": restored_record,
        "derived_not_from_boolean": derived_record,
        "c8_digest_differs": (share_record["c8"]["state_digest"]
                              != refusal_record["c8"]["state_digest"]),
        "hashes": {
            str(path.relative_to(RETURN)): _sha(path)
            for path in (
                RETURN / "candidate/vendor/bp2/bp2_joined/material_source.py",
                RETURN / "candidate/vendor/bp2/bp2_joined/binding.py",
                RETURN / "candidate/vendor/bp2/bp2_joined/producer.py",
                RETURN / "candidate/vendor/bp2/bp2_joined/__init__.py",
                RETURN / "candidate/vendor/bp2/bp2_joined/bootstrap.py",
                RETURN / "firstclass.py",
                RETURN / "install.py",
                RETURN / "tests/test_firstclass_b_source.py",
            )
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
