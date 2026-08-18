#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import types
import unicodedata
from pathlib import Path

import pandas as pd
import pytest

# The DB module exposes pure mapping/SQL-contract helpers used here. Keep these
# regressions executable on clean test hosts that do not install the optional
# live-Postgres client; no DB call is made by this test module.
if importlib.util.find_spec("psycopg2") is None:
    psycopg2_stub = types.ModuleType("psycopg2")
    psycopg2_stub.connect = lambda *_args, **_kwargs: (_ for _ in ()).throw(
        RuntimeError("psycopg2 unavailable in unit-test environment")
    )
    psycopg2_extras_stub = types.ModuleType("psycopg2.extras")
    psycopg2_extras_stub.execute_values = lambda *_args, **_kwargs: None
    sys.modules["psycopg2"] = psycopg2_stub
    sys.modules["psycopg2.extras"] = psycopg2_extras_stub
if importlib.util.find_spec("dotenv") is None:
    dotenv_stub = types.ModuleType("dotenv")
    dotenv_stub.load_dotenv = lambda *_args, **_kwargs: False
    sys.modules["dotenv"] = dotenv_stub

from data.ddm_build_copy import apply_postgres_facet_ready_substrate as db
from data.ddm_build_copy import build_question_structure_register as qsr
from data.ddm_build_copy import build_source_structure_validator as validator
from data.ddm_build_copy.ddm_source_wave_identity import (
    CLOSED_35,
    RECOGNIZED_EXCLUDED,
    closed_35_identities,
    resolve_source_wave_identity,
)

ROOT = Path(__file__).resolve().parents[3]
BINDINGS = ROOT / "data" / "ddm_build_copy" / "bindings"

PINNED_GIT_BLOBS = {
    "wave_authority_registry_35wave_v1.json": "784c6cc3587cf09788e4cf831f1a66bf4af3e843",
    "question_relation_registry_35wave_active_v1.yaml": "cd7e0c4bf1a5148ce11fac0461c8e185877a44a3",
    "question_relation_registry_35wave_active_v1.schema.json": "c020aea9ae443104dd5e3f279366e647e3ea31bf",
    "question_block_registry_35wave_active_v1.yaml": "37288223e26db8db1cc188b99173ecea44aeb616",
    "relation_axis_registry_35wave_active_v1.yaml": "0c34db3bbd4f007ffdcfd2290c0888745c6f9ae5",
    "structural_domain_registry_35wave_active_v1.yaml": "1c4ee3017d28551f80bc6f988e11c87392aaac17",
    "target_entity_registry_35wave_active_v1.yaml": "8471d721e125c4c094f6d9f456c920d804a97768",
    "question_relation_registry.csv": "8b651995ec8c5527cb9e5a87734ea289fdf2fa9e",
    "question_relation_registry.yaml": "ec42b9b23c002d04d5c545c369dca1a901b6db69",
    "question_relation_registry_35wave_active_v1.csv": "daac001bb8da645c7d99408e2239f4e04b6e9f9b",
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_pinned_companion_bytes_and_active_qra_are_exact():
    for name, expected in PINNED_GIT_BLOBS.items():
        path = BINDINGS / name
        assert path.is_file(), name
        assert git_blob_sha1(path) == expected, name


def test_closed_35_uid_census_is_exact_and_asian_w6_is_excluded():
    identities = closed_35_identities()
    assert len(identities) == 35
    assert len({identity.wave_uid for identity in identities}) == 35
    assert all(identity.governance_state == CLOSED_35 for identity in identities)
    assert all(identity.closed_35_member for identity in identities)
    w6 = resolve_source_wave_identity("Asian Barometer", "Wave 6")
    assert w6.wave_uid == "wv_asian_barometer_w6_v1"
    assert w6.governance_state == RECOGNIZED_EXCLUDED
    assert not w6.closed_35_member
    assert w6.wave_uid not in {identity.wave_uid for identity in identities}


def test_arab_aliases_and_latinobarometro_nfc_nfd_resolve_identically():
    arab = {resolve_source_wave_identity("Arab Barometer", value).wave_uid for value in ["I", "W1", "Wave 1", "1"]}
    assert arab == {"wv_arab_barometer_i_v1"}
    nfc = "Latinobarómetro"
    nfd = unicodedata.normalize("NFD", nfc)
    assert nfc != nfd
    a = resolve_source_wave_identity(nfc, "1995")
    b = resolve_source_wave_identity(nfd, "1995")
    c = resolve_source_wave_identity("Latinobarometro", "1995")
    assert {a.source_family_uid, b.source_family_uid, c.source_family_uid} == {"sf_latinobarometro_v1"}
    assert {a.wave_uid, b.wave_uid, c.wave_uid} == {"wv_latinobarometro_1995_v1"}


def _synthetic_validation_rows(*, drop_uid: str | None = None, include_w6: bool = False):
    rows = []
    for identity in closed_35_identities():
        if identity.wave_uid == drop_uid:
            continue
        rows.append({
            "dataset_id": f"dataset::{identity.wave_uid}",
            "raw_source": identity.canonical_display_source,
            "raw_wave": identity.canonical_display_wave,
            "canonical_display_source": identity.canonical_display_source,
            "canonical_display_wave": identity.canonical_display_wave,
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "governance_state": identity.governance_state,
            "closed_35_member": True,
            "audit_csv": f"data/ddm_build_copy/reports/source_structure_audits/{identity.wave_uid}.csv",
            "audit_sha256": "a" * 64,
            "raw_path": f"/legacy/{identity.wave_uid}.sav",
            "codebook_path": f"/legacy/{identity.wave_uid}.csv",
        })
    if include_w6:
        w6 = resolve_source_wave_identity("Asian Barometer", "W6")
        rows.append({
            "dataset_id": "dataset::asian-w6",
            "raw_source": "Asian Barometer",
            "raw_wave": "W6",
            "canonical_display_source": "Asian Barometer",
            "canonical_display_wave": "W6",
            "source_family_uid": w6.source_family_uid,
            "wave_uid": w6.wave_uid,
            "governance_state": w6.governance_state,
            "closed_35_member": False,
            "audit_csv": "data/ddm_build_copy/reports/source_structure_audits/asian-w6.csv",
            "audit_sha256": "b" * 64,
        })
    return rows


def test_binding_publication_requires_all_35_and_never_promotes_asian_w6():
    complete = validator.build_audit_binding(_synthetic_validation_rows(include_w6=True))
    assert complete["status"] == validator.READY_BINDING_STATUS
    assert complete["observed_wave_uid_count"] == 35
    assert "wv_asian_barometer_w6_v1" not in complete["observed_wave_uids"]
    missing_uid = closed_35_identities()[0].wave_uid
    partial = validator.build_audit_binding(_synthetic_validation_rows(drop_uid=missing_uid))
    assert partial["status"] != validator.READY_BINDING_STATUS
    assert missing_uid not in partial["observed_wave_uids"]
    assert any("missing_wave_uids:" in blocker for blocker in partial["blockers"])


def test_checked_in_binding_is_explicitly_not_green_until_hash_bound_republication():
    payload = json.loads((ROOT / "data" / "ddm_build_copy" / "manifests" / "source_structure_audit_binding_35wave_v1.json").read_text(encoding="utf-8"))
    assert payload["expected_wave_uid_count"] == 35
    assert payload["status"] != qsr.READY_BINDING_STATUS
    assert payload["artifacts"] == []
    with pytest.raises(RuntimeError, match="SOURCE_STRUCTURE_BINDING_NOT_READY"):
        qsr.load_audit_binding()


def _ready_binding(tmp_path: Path):
    artifacts = []
    payload = b"record_kind,name,classification_kind,structural_role\ncodebook_row,q1,single_choice,answer\n"
    audit_file = tmp_path / "shared.csv"
    audit_file.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    expected = []
    for identity in closed_35_identities():
        expected.append(identity.wave_uid)
        artifacts.append({
            "dataset_id": f"dataset::{identity.wave_uid}",
            "raw_source": identity.canonical_display_source,
            "raw_wave": identity.canonical_display_wave,
            "canonical_display_source": identity.canonical_display_source,
            "canonical_display_wave": identity.canonical_display_wave,
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "governance_state": identity.governance_state,
            "closed_35_member": True,
            "audit_file": "shared.csv",
            "audit_sha256": digest,
        })
    return {
        "schema": qsr.BINDING_SCHEMA,
        "status": qsr.READY_BINDING_STATUS,
        "expected_wave_uids": sorted(expected),
        "observed_wave_uids": sorted(expected),
        "artifacts": artifacts,
    }


def test_portable_hash_bound_audits_need_no_desktop_or_legacy_absolute_path(tmp_path):
    binding = _ready_binding(tmp_path)
    resolved = qsr.resolve_bound_audit_artifacts(binding, root=tmp_path)
    assert len(resolved) == 35
    assert all(path.parent == tmp_path for _artifact, path in resolved)
    assert "/Users/" not in json.dumps(binding)
    bad = json.loads(json.dumps(binding))
    bad["artifacts"][0]["audit_file"] = "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build/reports/source_structure_audits/shared.csv"
    with pytest.raises(RuntimeError, match="NONPORTABLE_PATH"):
        qsr.resolve_bound_audit_artifacts(bad, root=tmp_path)


def test_duplicate_wave_uid_cannot_satisfy_exact_35_binding(tmp_path):
    binding = _ready_binding(tmp_path)
    binding["artifacts"][-1] = dict(binding["artifacts"][0])
    with pytest.raises(RuntimeError, match="DUPLICATE_WAVE_UID|UID_COVERAGE_MISMATCH"):
        qsr.resolve_bound_audit_artifacts(binding, root=tmp_path)


def test_missing_one_wave_and_partial_nonempty_qsr_cannot_publish_green():
    rows = [{"wave_uid": identity.wave_uid, "closed_35_member": True} for identity in closed_35_identities()]
    assert qsr.validate_qsr_publication_scope(pd.DataFrame(rows))["wave_uid_count"] == 35
    with pytest.raises(RuntimeError, match="UID_COVERAGE_MISMATCH"):
        qsr.validate_qsr_publication_scope(pd.DataFrame(rows[:-1]))


def test_qsr_identity_context_preserves_raw_display_and_uid_separately():
    evs = resolve_source_wave_identity("EVS", "W1")
    artifact = {
        "dataset_id": "evs-w1",
        "raw_source": "EVS",
        "raw_wave": "W1",
        "canonical_display_source": evs.canonical_display_source,
        "canonical_display_wave": evs.canonical_display_wave,
        "source_family_uid": evs.source_family_uid,
        "wave_uid": evs.wave_uid,
        "governance_state": evs.governance_state,
        "closed_35_member": True,
        "audit_sha256": "a" * 64,
        "legacy_raw_path_provenance": "/Users/matthewsmith/Desktop/Rawlsing/data/EVS/raw.sav",
    }
    context = qsr.identity_context_from_artifact(
        artifact,
        {"source_family": "EVS", "wave": "1981", "canonical_wave": "W1"},
    )
    assert context["raw_wave"] == "W1"
    assert context["wave"] == "1981"
    assert context["canonical_wave"] == "W1"
    assert context["canonical_display_wave"] == "1981"
    assert context["wave_uid"] == "wv_evs_1981_v1"
    assert context["raw_path"].startswith("/Users/")


def test_db_mapping_preserves_qsm_compatibility_wave_beside_uid_and_respondent_uid_join():
    frame = pd.DataFrame([{
        "source": "EVS", "wave": "W1", "var_name": "Q1", "display_text": "Example",
        "final_driver_id": "driver-1", "mapping_status": "accepted_existing_mapping",
    }])
    row = db.create_question_mapping_rows(frame)[0]
    assert row[0] == "EVS"
    assert row[1] == "W1"
    assert row[2] == "sf_evs_v1"
    assert row[3] == "wv_evs_1981_v1"
    assert row[4] == "EVS"
    assert row[5] == "1981"
    sql = db.FACET_READY_VIEW_SQL
    assert "rsi.raw_db_source = r.source" in sql
    assert "rsi.raw_db_wave = COALESCE(r.wave, '')" in sql
    assert "q.source_family_uid = rsi.source_family_uid" in sql
    assert "q.wave_uid = rsi.wave_uid" in sql
    assert "NULLIF(rsi.wave_uid, '') IS NULL" in sql
    assert "NULLIF(q.wave_uid, '') IS NULL" in sql
    assert "COALESCE(q.wave, '') = ''" in sql
    assert "q.wave = COALESCE(r.wave, '')" not in sql
    assert "q.canonical_display_wave = COALESCE(r.wave, '')" not in sql
    assert "r.wave AS raw_db_wave" in sql


def test_db_identity_normalization_does_not_mutate_question_mapping_semantics():
    original = {
        "source": "Arab Barometer", "wave": "W1", "var_name": "QX", "display_text": "Text",
        "final_driver_id": "FD", "final_driver_label": "Label", "final_driver_scope": "Scope",
        "final_driver_origin": "Origin", "driver_id": "D", "driver_facet_id": "F",
        "question_block_id": "B", "structural_domain_id": "S", "relation_axis_id": "R",
        "target_entity_id": "T", "mapping_status": "accepted", "evidence_kind": "kind",
        "strata_relevance": "strata", "channel_affordances": "channel",
        "forbidden_inference": "forbid", "does_not_measure": "does-not", "review_notes": "note",
    }
    row = db.create_question_mapping_rows(pd.DataFrame([original]))[0]
    assert row[0:2] == ("Arab Barometer", "W1")
    assert row[2] == "sf_arab_barometer_v1"
    assert row[3] == "wv_arab_barometer_i_v1"
    assert row[5] == "I"
    assert row[10:] == (
        "Text", "FD", "Label", "Scope", "Origin", "D", "F", "B", "S", "R", "T",
        "accepted", "kind", "strata", "channel", "forbid", "does-not", "note",
    )


def test_qra_semantic_authority_file_is_exactly_unchanged():
    qra = BINDINGS / "question_relation_registry_35wave_active_v1.csv"
    assert git_blob_sha1(qra) == "daac001bb8da645c7d99408e2239f4e04b6e9f9b"
