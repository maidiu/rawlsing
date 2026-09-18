from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import inspect
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "WORKER_RETURNS" / "EE-P2R6J"
SUPPORT = OUT / "SUPPORT"
R6L = ROOT / "WORKER_RETURNS" / "EE-P2R6L" / "RUN_OUTPUT"
ISSUER = OUT / "02_CORRECTED_BINDING_ISSUER.py"
SNAPSHOT = SUPPORT / "00_CURRENT_BINDING_REGISTRY_SNAPSHOT.json"
OLD = SUPPORT / "01_QUARANTINED_R6I_CANDIDATE.json"

R5_REL = ROOT / "WORKER_RETURNS" / "EE-P2R5A" / "02_RELEASE_REALIZATION_RELATION_AUTHORITY.json"
R5_SCHEMA = ROOT / "WORKER_RETURNS" / "EE-P2R5A" / "03_CONCRETE_REALIZATION_BINDING_SCHEMA.json"
R5_CLAUSE = ROOT / "WORKER_RETURNS" / "EE-P2R5A" / "04_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE.json"
FIX = ROOT / "rawlsing_next" / "tests" / "fixtures"
R4 = {
    "dialect": FIX / "ee_p2r6a_r4a_01_dialect.json",
    "respondent": FIX / "ee_p2r6a_r4a_02_respondent.json",
    "mixed": FIX / "ee_p2r6a_r4a_03_mixed.json",
    "derived": FIX / "ee_p2r6a_r4a_04_derived.json",
    "successor": FIX / "ee_p2r6a_r4a_05_successor.json",
}

PRODUCTION = ROOT / "rawlsing_next" / "pre553_runtime_authority.py"
REPOSITORY_MODULE = ROOT / "rawlsing_next" / "pre553_c11_repository.py"

EXPECTED_RUN_OUTPUT = {
    "successor_release_extension_scan.json",
    "successor_release_m01_m18.json",
    "successor_release_receipt.json",
    "successor_release_replay_manifest.json.zip",
}
ADOPTED = (
    "3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74",
    "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55",
    "225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4",
    "b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae",
    "9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5",
    "a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0",
    "d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e",
    "d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2",
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path):
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def runtime(data, bindings):
    from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet
    return Pre553RuntimeAuthoritySet(
        adopted_authority_hashes=ADOPTED,
        predicate_dialect_matrices=(data["dialect"],),
        respondent_compatibility_authorities=(data["respondent"],),
        mixed_composition_authorities=(data["mixed"],),
        derived_predicate_contracts=(data["derived"],),
        public_predicate_successor_authorities=(data["successor"],),
        release_realization_authorities=(data["realization"],),
        realization_binding_schemas=(data["schema"],),
        release_precondition_clauses=(data["clause"],),
        realization_bindings=bindings,
    )


def blocker_receipt(candidate, active, mismatch):
    receipt = load(R6L / "successor_release_receipt.json")
    return {
        "schema": "EE_P2R6J_R6A_PRODUCTION_RUNTIME_VERIFICATION_RECEIPT@1.0.0",
        "disposition": "BLOCKED_BEFORE_EXACT_POSITIVE_PRODUCTION_RUNTIME_CALL",
        "blocker": "EXACT_ADOPTED_R6L_C11REPOSITORY_RELEASE_NOT_REHYDRATABLE_FROM_COMMITTED_ADOPTED_ARTIFACTS_WITHOUT_SOURCE_OR_CARRIER_ACCESS",
        "production_runtime": {
            "module": "rawlsing_next/pre553_runtime_authority.py",
            "git_blob_sha1": "2ddc591f2572983d18f8f3e8f81a33b80b3bca7b",
            "entrypoint": "Pre553RuntimeAuthoritySet.require_realized_release",
            "modified": False,
        },
        "corrected_binding_hash": active["binding_ref"]["content_hash"],
        "corrected_binding_ref": active["binding_ref"],
        "identity_material_field_count": len(active["identity_material"]),
        "identity_material_fields": list(active["identity_material"].keys()),
        "r6i_contract_mismatch_proved": True,
        "quarantined_r6i_hash": "fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0",
        "r6l_committed_run_output_files": sorted(EXPECTED_RUN_OUTPUT),
        "r6l_runtime_release_ref": receipt["accepted_i02_successor"]["release_ref"],
        "r6l_record_counts": receipt["accepted_i02_successor"]["record_counts"],
        "repository_release_count_previously_proved_by_r6l": receipt["accepted_i02_successor"]["repository_release_count"],
        "repository_exact_resolution_previously_proved_by_r6l": receipt["accepted_i02_successor"]["resolve_release_exact"],
        "exact_positive_call_executed": False,
        "reason_positive_call_not_executed": "Production C11Repository accepts only I02-sealed C11LogicalRelease objects. Adopted repository artifacts preserve release/replay identities and closure refs but not the validated public/internal member bodies required to reconstruct that exact sealed release. Calling the private seal with omitted/fabricated bodies would be a fake repository.",
        "fake_repository_or_private_seal_substitution_used": False,
        "source_or_carrier_access": False,
        "a_b_qualification": False,
        "be1_or_p2x": False,
        "mismatch_missing_required_fields": mismatch["missing_required_fields"],
    }


def test_ee_p2r6j_contract_alignment_and_exact_repository_blocker_payload():
    assert git_blob_sha1(PRODUCTION) == "2ddc591f2572983d18f8f3e8f81a33b80b3bca7b"
    assert git_blob_sha1(REPOSITORY_MODULE) == "67c6eb6494522cd11aab1b93d0e73f9cef6036f3"
    assert {p.name for p in R6L.iterdir() if p.is_file()} == EXPECTED_RUN_OUTPUT
    assert git_blob_sha1(R6L / "successor_release_receipt.json") == "0e076af954f2da0591a6881f6445150e17c3b48d"
    assert git_blob_sha1(R6L / "successor_release_m01_m18.json") == "9d810e33ccf7d07526c11a584262a85ed1b5c27f"
    assert git_blob_sha1(R6L / "successor_release_extension_scan.json") == "6412d1aadf44a9273a39ea04cdbd5727592e2ece"
    assert git_blob_sha1(R6L / "successor_release_replay_manifest.json.zip") == "d20b8aeee5abe5a1348e5ab17546c82e3592ab6e"
    assert sha256_file(R6L / "successor_release_replay_manifest.json.zip") == "9d2c608f21d9d93111c7418bce945f6245340389d7e8c2ccff70b18af358dd70"

    issuer = import_path("ee_p2r6j_issuer", ISSUER)
    schema, relation, receipt = load(R5_SCHEMA), load(R5_REL), load(R6L / "successor_release_receipt.json")
    snapshot, old = load(SNAPSHOT), load(OLD)
    candidate, active = issuer.issue(
        binding_schema=schema,
        relation_authority=relation,
        r6l_receipt=receipt,
        binding_registry_snapshot=snapshot,
        quarantined_r6i_candidate=old,
    )

    from rawlsing_next.pre553_empirical_objects import exact_ref, semantic_hash
    from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
    from rawlsing_next.pre553_c11_repository import C11Repository
    assert tuple(active["identity_material"].keys()) == issuer.REQUIRED_FIELDS
    assert len(active["identity_material"]) == 17
    assert semantic_hash(active["identity_material"]) == active["binding_ref"]["content_hash"]
    assert active["binding_ref"]["content_hash"] != issuer.QUARANTINED_R6I_HASH
    assert active["schema"] == "RELEASE_REALIZATION_BINDING@1.0.0"
    assert active["typed_state"] == "ACTIVE_POSITIVE"

    required = set(schema["future_binding_required_fields"])
    old_fields = set(old["identity_material"])
    present = sorted(required & old_fields)
    missing = sorted(required - old_fields)
    assert present == sorted([
        "accepted_base_i02_release_ref", "frozen_scope_anchor_ref",
        "relation_authority_ref", "runtime_i02_release_ref",
    ])
    assert len(missing) == 13
    mismatch = {
        "schema": "EE_P2R6J_STATIC_R6I_R6A_CONTRACT_MISMATCH_PROOF@1.0.0",
        "disposition": "PROVED",
        "r6a_production_blob": "2ddc591f2572983d18f8f3e8f81a33b80b3bca7b",
        "r5a_binding_schema_blob": "00159aae4117c00d9dfcc7e9b558e1c1d1637302",
        "required_field_count": 17,
        "r6i_exact_required_fields_present": present,
        "r6i_exact_required_field_count_present": 4,
        "missing_required_fields": missing,
        "missing_required_field_count": 13,
        "quarantined_candidate_hash": issuer.QUARANTINED_R6I_HASH,
    }

    # Exact production contract behavior can be tested negatively without source/carriers.
    data = {
        "dialect": load(R4["dialect"]), "respondent": load(R4["respondent"]),
        "mixed": load(R4["mixed"]), "derived": load(R4["derived"]),
        "successor": load(R4["successor"]), "realization": relation,
        "schema": schema, "clause": load(R5_CLAUSE),
    }
    scope = exact_ref(schema["future_binding_required_fields"]["frozen_scope_anchor_ref"])
    runtime_ref = exact_ref(receipt["accepted_i02_successor"]["release_ref"])
    empty_repo = C11Repository()

    with pytest.raises(Pre553AuthorityError, match="zero active positive"):
        runtime(data, ()).require_realized_release(scope, repository=empty_repo, runtime_release_ref=runtime_ref)
    with pytest.raises(Pre553AuthorityError, match="multiple active positive"):
        runtime(data, (active, copy.deepcopy(active))).require_realized_release(
            scope, repository=empty_repo, runtime_release_ref=runtime_ref
        )

    old_active = {
        "schema": "RELEASE_REALIZATION_BINDING@1.0.0",
        "typed_state": "ACTIVE_POSITIVE",
        "binding_ref": {
            "kind": "ReleaseRealizationBinding@1.0.0",
            "object_id": "urn:rawlsing:prev3:p2r6j:quarantined-proof:" + old["binding_ref"]["content_hash"],
            "content_hash": semantic_hash(old["identity_material"]),
        },
        "identity_material": copy.deepcopy(old["identity_material"]),
    }
    old_active["binding_ref"]["content_hash"] = semantic_hash(old_active["identity_material"])
    with pytest.raises(Pre553AuthorityError, match="is required"):
        runtime(data, (old_active,)).require_realized_release(
            scope, repository=empty_repo, runtime_release_ref=runtime_ref
        )

    bad_source = copy.deepcopy(active)
    bad_source["identity_material"]["source_artifact_sha256"] = "0" * 64
    bad_source["binding_ref"]["content_hash"] = semantic_hash(bad_source["identity_material"])
    bad_source["binding_ref"]["object_id"] = "urn:rawlsing:prev3:p2r6j:bad-source:" + bad_source["binding_ref"]["content_hash"]
    with pytest.raises(Pre553AuthorityError):
        runtime(data, (bad_source,)).require_realized_release(
            scope, repository=empty_repo, runtime_release_ref=runtime_ref
        )

    bad_required = copy.deepcopy(active)
    bad_required["identity_material"]["selector_refs"][0] = "0" * 64
    bad_required["binding_ref"]["content_hash"] = semantic_hash(bad_required["identity_material"])
    bad_required["binding_ref"]["object_id"] = "urn:rawlsing:prev3:p2r6j:bad-selector:" + bad_required["binding_ref"]["content_hash"]
    with pytest.raises(Pre553AuthorityError, match="does not match exact adopted binding schema"):
        runtime(data, (bad_required,)).require_realized_release(
            scope, repository=empty_repo, runtime_release_ref=runtime_ref
        )

    # The structurally corrected record reaches the exact repository lookup and
    # fails only because no lawful exact R6L sealed release is reconstructable here.
    with pytest.raises(Pre553AuthorityError, match="absent from exact C11Repository"):
        runtime(data, (active,)).require_realized_release(
            scope, repository=empty_repo, runtime_release_ref=runtime_ref
        )

    repo_source = REPOSITORY_MODULE.read_text(encoding="utf-8")
    assert "repository accepts only I02-validated sealed C11LogicalRelease" in repo_source
    assert "def resolve_release_exact" in repo_source
    assert "latest" not in "\n".join(
        line for line in repo_source.splitlines() if line.lstrip().startswith("def resolve_")
    )
    assert "_make_validated_release" in repo_source

    with tempfile.TemporaryDirectory(prefix="ee-p2r6j-") as td:
        td = Path(td)
        replay = td / "successor_release_replay_manifest.json"
        with zipfile.ZipFile(R6L / "successor_release_replay_manifest.json.zip") as zf:
            infos = zf.infolist()
            assert len(infos) == 1 and infos[0].filename == replay.name
            with zf.open(infos[0]) as src, replay.open("wb") as dst:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)
        assert replay.stat().st_size == 118508673
        assert sha256_file(replay) == "aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5"
        manifest = load(replay)
        assert manifest["record_family"] == "ReplayManifest"
        assert manifest["content_hash"] == "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
        assert "public_objects" not in manifest and "internal_records" not in manifest

    verification = blocker_receipt(candidate, active, mismatch)
    payload = {
        "mismatch": mismatch,
        "candidate": candidate,
        "active": active,
        "verification": verification,
    }

    # First governed run intentionally surfaces exact deterministic artifacts.
    committed = OUT / "03_CORRECTED_RUNTIME_BINDING_CANDIDATE.json"
    if not committed.exists():
        encoded = base64.b64encode(canonical(payload).encode("utf-8")).decode("ascii")
        raise AssertionError("EE_P2R6J_PAYLOAD_B64=" + encoded)

    assert canonical(load(OUT / "01_STATIC_R6I_R6A_CONTRACT_MISMATCH_PROOF.json")) == canonical(mismatch)
    assert canonical(load(OUT / "03_CORRECTED_RUNTIME_BINDING_CANDIDATE.json")) == canonical(candidate)
    assert canonical(load(OUT / "04_PROPOSED_ACTIVE_RUNTIME_BINDING_RECORD.json")) == canonical(active)
    assert canonical(load(OUT / "05_R6A_PRODUCTION_RUNTIME_VERIFICATION_RECEIPT.json")) == canonical(verification)
