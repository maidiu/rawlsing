#!/usr/bin/env python3
"""EE-P2R6B deterministic concrete ReleaseRealizationBinding candidate issuer.

This module is Browser-prepared only. Production issuance is impossible unless an
exact EE-P2R5B successor-release receipt passes the adopted R5B verifier and all
R5A authority/uniqueness inputs close. Structural fixtures use a disjoint
NONEMPIRICAL__NONBINDING schema and can never become production bindings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
R5B_VERIFIER = HERE / "02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py"

R5B_VERIFIER_GIT_BLOB_SHA1 = "e7752c558c7fb407852ef7377f45eca775d3b86b"
R5B_RECEIPT_SCHEMA_GIT_BLOB_SHA1 = "d76e0475258ca8a37958fadc956356dc68749e08"
R5B_RETURN_HEAD = "648a39ad5bed42f66e066410af5869604d29c12d"

HQ_CHECKPOINT = "20260918T1553-0400"
HQ_HANDOFF = "9cbd963ef4d1f2243543df4ec61d80368364c449"
HQ_DECISION = "HQD-2026-09-18-046"
R5A_RETURN_HEAD = "6586da01edac5e87fb81b6beb8d7b16fc0ea18ef"

RELATION_AUTHORITY_HASH = "9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5"
BINDING_SCHEMA_HASH = "a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0"
R4A_SUCCESSOR_CLAUSE_HASH = "d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e"
R5A_AGGREGATE_HASH = "d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2"
R4A_AGGREGATE_HASH = "b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae"
AUTHORITY_EPOCH_ID = "30815cfb20f4f66140cee8f6a2b5e5cafd5e20fb4d1b0c607bad1e3699fae2ff"

SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
FROZEN_SCOPE_HASH = "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
BASE_RELEASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
BASE_REPLAY_HASH = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"

FROZEN_SCOPE_REF = {
    "kind": "C11LogicalRelease",
    "object_id": "LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669",
    "content_hash": FROZEN_SCOPE_HASH,
}
BASE_RELEASE_REF = {
    "kind": "C11LogicalRelease",
    "object_id": "LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79",
    "content_hash": BASE_RELEASE_HASH,
}

RELATION_AUTHORITY_REF = {
    "kind": "ReleaseRealizationAuthorityCandidate@1.0.0",
    "object_id": f"urn:rawlsing:prev3:p2r5a:release-realization-authority:sha256:{RELATION_AUTHORITY_HASH}",
    "content_hash": RELATION_AUTHORITY_HASH,
}
BINDING_SCHEMA_REF = {
    "kind": "ReleaseRealizationBindingSchema@1.0.0",
    "object_id": f"urn:rawlsing:prev3:p2r5a:release-realization-binding-schema:sha256:{BINDING_SCHEMA_HASH}",
    "content_hash": BINDING_SCHEMA_HASH,
}
R4A_SUCCESSOR_CLAUSE_REF = {
    "kind": "R4AReleasePreconditionSuccessorClauseCandidate@1.0.0",
    "object_id": f"urn:rawlsing:prev3:p2r5a:r4a-release-precondition:sha256:{R4A_SUCCESSOR_CLAUSE_HASH}",
    "content_hash": R4A_SUCCESSOR_CLAUSE_HASH,
}
R5A_AGGREGATE_REF = {
    "kind": "ReleaseRealizationSuccessorAuthorityCandidate@1.0.0",
    "object_id": f"urn:rawlsing:prev3:p2r5a:release-realization-successor:sha256:{R5A_AGGREGATE_HASH}",
    "content_hash": R5A_AGGREGATE_HASH,
}

R4A_AUTHORITY_HASHES = {
    "respondent_binding": "3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74",
    "mixed_grammar": "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55",
    "derived_predicate": "225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4",
    "aggregate": R4A_AGGREGATE_HASH,
}

EXPECTED_SELECTORS = {
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:1": "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:2": "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:3": "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:1": "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:2": "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:3": "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}

EXPECTED_Q = {
    "q310": {
        "question_ref": "c4b0f76b7a37d8083a103ffd316f2eb009eeca7b5cbf5910e51d364b39641534",
        "response_slot_ref": "fa63b7f74c1fc2c587b485031f0ee841abcaff964368c6eb33862da34b198593",
        "routing_ref": "5799578dfbe21f2997578a43edae97c4818f693ee85ed3d345cdc4574374e013",
        "response_value_state_refs": {
            "1": "e94b7665fffc55b564c33b139bc8a1608d381f89e81b63d99db42c9129a697da",
            "2": "23589e5578c5a80749600bb3e4385705e8ac0f8d4297c2faaac457b0ce5f0ed4",
            "3": "fe9fc4a890814f6b2f4882fc4c4127f27091b704fc9ce1eb90392173556f60e1",
            "MISSING": "57af6ec1e41dfbb7c4d9946dcad5c34c58526bc239c012d8cda22c6ae1975244",
        },
    },
    "q311": {
        "question_ref": "8680064d936efb99d64457edc3a2385e8862a2aac6bf50efd423afe83e77aed9",
        "response_slot_ref": "0d1ff28f5bf8200920c596449229c5e965ba407cadc4f54ec3292e204a1220e7",
        "routing_ref": "fc7530bf63bd3662d0f49545363947e1f18379ecd03583de9cc7ca2845d318bf",
        "response_value_state_refs": {
            "1": "09d12eb8563ed35b371bddc5829c3bd85b1acd0aa4a4f30fbe6795a0a0588234",
            "2": "dc457fb064cfcab1d353ab3032a48519e5a62f003d32b6b1b240c79d51578775",
            "3": "4492fc52c88c0a11c0ccfc45521879a53c46fab843808032cd1ccf061d995641",
            "MISSING": "02aef63755380ce3c6b54350282dd79d789264999943e1c18dec6ddc77ffb392",
        },
    },
}
EXPECTED_F02_AUTHORITIES = {
    "source_semantics": {
        "authority_id": "urn:rawlsing:prev3:f02:lits1:source-semantics",
        "authority_version": "1.0.0",
        "authority_content_hash": "47142de560f66e725283aaf96024bfad06fb0b33eeb56e3c8cfdc8afcc745bc0",
    },
    "routing": {
        "authority_id": "urn:rawlsing:prev3:f02:lits1:routing",
        "authority_version": "1.0.0",
        "authority_content_hash": "52e741a07b75c475254628dfdf191a77f969e0a7cd7bbdf9b7a90addf324d540",
    },
    "predicate_grammar": {
        "authority_id": "urn:rawlsing:prev3:f02:lits1:predicate-grammar",
        "authority_version": "1.0.0",
        "authority_content_hash": "bc6d433ff58e67e343f1bd1d8e3e92d691b81931dca6447716b08dbf0c8eff8b",
    },
    "replay": {
        "authority_id": "urn:rawlsing:prev3:f02:lits1:replay",
        "authority_version": "1.0.0",
        "authority_content_hash": "0b2ac266ec09db440156e3c1ab62dec2aac78290932d20396b753ca8763c9e4c",
    },
}

EXPECTED_EXTENSION_KEYS = {
    "projection_material", "question_and_member_refs", "authority_refs", "selector_refs",
    "source_scan_receipt_file", "source_scan_receipt_sha256", "question_binding_refs",
    "event_count", "routing_count",
}
EXPECTED_SCAN_KEYS = {
    "schema", "source_sha256", "row_coordinate_relation", "source_scan",
    "extension_event_ref_root_sha256", "extension_routing_ref_root_sha256",
    "extension_event_count", "extension_routing_count", "f02_questions",
    "selector_refs", "authority_refs", "negative_ceiling",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_RESOLUTION_WORDS = ("latest", "default", "fuzzy", "nearest")

class IssuerError(ValueError):
    pass

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def sha256_obj(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise IssuerError(message)

def require_sha(value: Any, name: str) -> str:
    require(isinstance(value, str) and bool(SHA256_RE.fullmatch(value)), f"{name} must be lowercase sha256")
    return value

def require_exact_ref(value: Any, name: str, *, kind: str | None = None) -> dict[str, str]:
    require(isinstance(value, Mapping), f"{name} must be exact-ref object")
    require(set(value) == {"kind", "object_id", "content_hash"}, f"{name} exact-ref keys mismatch")
    require(isinstance(value.get("kind"), str) and value["kind"], f"{name}.kind missing")
    require(isinstance(value.get("object_id"), str) and value["object_id"], f"{name}.object_id missing")
    require_sha(value.get("content_hash"), f"{name}.content_hash")
    if kind is not None:
        require(value["kind"] == kind, f"{name}.kind mismatch")
    return dict(value)

def require_authority_ref(value: Any, expected: Mapping[str, str], name: str) -> None:
    require(value == expected, f"{name} mismatch")

def normalized_selector_hashes(selector_refs: Any) -> dict[str, str]:
    require(isinstance(selector_refs, Mapping), "selector_refs must be mapping")
    require(set(selector_refs) == set(EXPECTED_SELECTORS), "exact six F02 selector IDs required")
    out: dict[str, str] = {}
    for selector_id, expected_hash in EXPECTED_SELECTORS.items():
        ref = require_exact_ref(selector_refs[selector_id], f"selector_refs[{selector_id}]")
        require(ref["content_hash"] == expected_hash, f"selector identity changed: {selector_id}")
        out[selector_id] = ref["content_hash"]
    return out

def normalized_q_members(value: Any, name: str) -> dict[str, Any]:
    require(isinstance(value, Mapping), f"{name} must be mapping")
    require(set(value) == {"q310", "q311"}, f"{name} must contain only q310/q311")
    out: dict[str, Any] = {}
    for q in ("q310", "q311"):
        got = value[q]
        require(isinstance(got, Mapping), f"{name}.{q} must be mapping")
        require(set(got) == {"question_ref", "response_slot_ref", "routing_ref", "response_value_state_refs"},
                f"{name}.{q} member keys mismatch")
        expected = EXPECTED_Q[q]
        for key in ("question_ref", "response_slot_ref", "routing_ref"):
            ref = require_exact_ref(got[key], f"{name}.{q}.{key}")
            require(ref["content_hash"] == expected[key], f"{name}.{q}.{key} changed")
        states = got["response_value_state_refs"]
        require(isinstance(states, Mapping) and set(states) == {"1", "2", "3", "MISSING"},
                f"{name}.{q}.response_value_state_refs mismatch")
        for state, expected_hash in expected["response_value_state_refs"].items():
            ref = require_exact_ref(states[state], f"{name}.{q}.response_value_state_refs.{state}")
            require(ref["content_hash"] == expected_hash, f"{name}.{q} response state changed: {state}")
        out[q] = json.loads(canonical_json(got))
    return out

def normalized_f02_authorities(value: Any, name: str) -> dict[str, Any]:
    require(value == EXPECTED_F02_AUTHORITIES, f"{name} exact F02 authority set mismatch")
    return json.loads(canonical_json(value))

def exact_epoch_material() -> dict[str, Any]:
    return {
        "schema": "EE_P2R6B_R5A_AUTHORITY_EPOCH@1.0.0",
        "hq_checkpoint": HQ_CHECKPOINT,
        "hq_handoff_commit": HQ_HANDOFF,
        "hq_decision": HQ_DECISION,
        "r5a_return_head": R5A_RETURN_HEAD,
        "realization_authority_hash": RELATION_AUTHORITY_HASH,
        "binding_schema_hash": BINDING_SCHEMA_HASH,
        "r4a_successor_clause_hash": R4A_SUCCESSOR_CLAUSE_HASH,
        "r5a_aggregate_hash": R5A_AGGREGATE_HASH,
        "r4a_aggregate_hash": R4A_AGGREGATE_HASH,
        "frozen_scope_anchor_hash": FROZEN_SCOPE_HASH,
        "source_sha256": SOURCE_SHA256,
        "accepted_base_release_hash": BASE_RELEASE_HASH,
    }

def uniqueness_key() -> str:
    return sha256_obj({
        "frozen_scope_anchor_hash": FROZEN_SCOPE_HASH,
        "source_sha256": SOURCE_SHA256,
        "authority_epoch_id": AUTHORITY_EPOCH_ID,
    })

def validate_authority_material(authority: Any) -> dict[str, Any]:
    require(isinstance(authority, Mapping), "authority material must be object")
    require(authority.get("schema") == "EE_P2R6B_ADOPTED_R5A_AUTHORITY_MATERIAL@1.0.0",
            "authority material schema mismatch")
    require(authority.get("status") == "ADOPTED_R5A_AUTHORITY_MATERIAL__PRE_BINDING",
            "authority material status mismatch")
    require(authority.get("authority_epoch") == exact_epoch_material(), "authority epoch material mismatch")
    require(sha256_obj(authority["authority_epoch"]) == AUTHORITY_EPOCH_ID, "authority epoch identity mismatch")
    require(authority.get("authority_epoch_id") == AUTHORITY_EPOCH_ID, "authority epoch id mismatch")
    refs = authority.get("adopted_refs", {})
    require_authority_ref(refs.get("release_realization_authority"), RELATION_AUTHORITY_REF, "release realization authority")
    require_authority_ref(refs.get("binding_schema"), BINDING_SCHEMA_REF, "binding schema")
    require_authority_ref(refs.get("r4a_successor_clause"), R4A_SUCCESSOR_CLAUSE_REF, "R4A successor clause")
    require_authority_ref(refs.get("r5a_aggregate"), R5A_AGGREGATE_REF, "R5A aggregate")
    require(authority.get("source_sha256") == SOURCE_SHA256, "authority source SHA mismatch")
    require(authority.get("frozen_scope_anchor_ref") == FROZEN_SCOPE_REF, "authority F02 anchor mismatch")
    require(authority.get("accepted_base_i02_release_ref") == BASE_RELEASE_REF, "authority base release mismatch")
    require(authority.get("accepted_base_replay_manifest_hash") == BASE_REPLAY_HASH, "authority base replay mismatch")
    require(authority.get("r4a_authority_hashes") == R4A_AUTHORITY_HASHES, "R4A authority closure mismatch")
    normalized_q_members(authority.get("f02_extension_refs"), "authority.f02_extension_refs")
    normalized_selector_hashes(authority.get("selector_refs"))
    normalized_f02_authorities(authority.get("f02_authority_refs"), "authority.f02_authority_refs")

    guard = authority.get("issuance_guard", {})
    require(guard == {
        "measured_outcomes_observed": False,
        "p2x_executed": False,
        "post_outcome_mutation": False,
        "runtime_release_hash_predeclared": False,
    }, "issuance guard mismatch/post-outcome mutation")

    inventory = authority.get("active_binding_inventory")
    require(isinstance(inventory, Mapping), "active binding inventory missing")
    require(inventory.get("schema") == "EE_P2R6B_ACTIVE_BINDING_INVENTORY@1.0.0",
            "active binding inventory schema mismatch")
    require(inventory.get("resolution_mode") == "EXACT_SCOPE_SOURCE_AUTHORITY_EPOCH",
            "binding inventory resolution must be exact")
    source_ref = require_exact_ref(inventory.get("inventory_source_ref"), "inventory_source_ref")
    require(source_ref["kind"] in {"HQAdoptedBindingRegistrySnapshot", "RepositoryBindingRegistrySnapshot"},
            "inventory source must be exact HQ/repository binding-registry snapshot")
    resolution_text = canonical_json({
        "resolution_mode": inventory.get("resolution_mode"),
        "inventory_source_ref": source_ref,
    }).lower()
    require(not any(word in resolution_text for word in FORBIDDEN_RESOLUTION_WORDS),
            "latest/default/fuzzy/nearest binding resolution forbidden")
    require(inventory.get("frozen_scope_anchor_hash") == FROZEN_SCOPE_HASH, "inventory scope mismatch")
    require(inventory.get("source_sha256") == SOURCE_SHA256, "inventory source mismatch")
    require(inventory.get("authority_epoch_id") == AUTHORITY_EPOCH_ID, "inventory epoch mismatch")
    require(inventory.get("uniqueness_key") == uniqueness_key(), "inventory uniqueness key mismatch")
    bindings = inventory.get("active_positive_bindings")
    require(isinstance(bindings, list), "active_positive_bindings must be list")
    count = inventory.get("active_positive_binding_count")
    require(isinstance(count, int) and count == len(bindings), "active binding inventory count mismatch")
    if count > 1:
        raise IssuerError("multiple active positive bindings for scope/source/authority epoch")
    if count == 1:
        raise IssuerError("pre-existing active positive binding exists; issuance requires exactly zero")
    require(count == 0, "issuance requires exactly zero pre-existing active bindings")
    inventory_material = {
        key: inventory[key]
        for key in (
            "schema", "resolution_mode", "inventory_source_ref", "frozen_scope_anchor_hash",
            "source_sha256", "authority_epoch_id", "uniqueness_key",
            "active_positive_bindings", "active_positive_binding_count",
        )
    }
    require(inventory.get("inventory_material_hash") == sha256_obj(inventory_material),
            "active binding inventory material hash mismatch")
    return json.loads(canonical_json(authority))

def run_exact_r5b_verifier(receipt_path: Path) -> dict[str, Any]:
    require(R5B_VERIFIER.is_file(), "exact vendored R5B verifier missing")
    require(git_blob_sha1(R5B_VERIFIER) == R5B_VERIFIER_GIT_BLOB_SHA1,
            "exact vendored R5B verifier Git blob mismatch")
    proc = subprocess.run(
        [sys.executable, str(R5B_VERIFIER), "--receipt", str(receipt_path)],
        text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise IssuerError(f"R5B verifier did not PASS: {detail}")
    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as exc:
        raise IssuerError("R5B verifier PASS output was not parseable JSON") from exc
    require(result.get("status") == "PASS", "R5B verifier output was not PASS")
    release_ref = require_exact_ref(result.get("accepted_i02_runtime_release_ref"),
                                    "R5B verifier runtime release", kind="C11LogicalRelease")
    require(result.get("r5a_realization_authority_claimed") is False, "R5B verifier reports realization claim")
    require(result.get("future_release_hash_was_not_predeclared") is True, "R5B verifier lacks non-predeclaration proof")
    return {"result": result, "runtime_release_ref": release_ref}

def validate_replay_manifest(path: Path, successor: Mapping[str, Any]) -> dict[str, Any]:
    replay = load_json(path)
    require(replay.get("record_family") == "ReplayManifest", "ReplayManifest record family mismatch")
    require(replay.get("record_version") == "1.0.0", "ReplayManifest version mismatch")
    require(isinstance(replay.get("semantic_fields"), Mapping), "ReplayManifest semantic_fields missing")
    projection = {
        "record_family": replay["record_family"],
        "record_version": replay["record_version"],
        "semantic_fields": replay["semantic_fields"],
    }
    expected_hash = sha256_obj(projection)
    require(replay.get("content_hash") == expected_hash, "ReplayManifest content hash mismatch")
    replay_ref = require_exact_ref(successor.get("replay_manifest_ref"), "successor.replay_manifest_ref")
    require(replay_ref["content_hash"] == expected_hash, "ReplayManifest ref/content mismatch")
    require(replay.get("object_id") == replay_ref["object_id"], "ReplayManifest object_id mismatch")
    require(replay["semantic_fields"].get("semantic_projection_hash") == successor.get("candidate_projection_hash"),
            "ReplayManifest does not close candidate projection")
    return replay

def validate_m01_m18(path: Path, successor: Mapping[str, Any]) -> dict[str, Any]:
    coverage = load_json(path)
    expected = {f"M{i:02d}" for i in range(1, 19)}
    require(isinstance(coverage, Mapping) and set(coverage) == expected, "M01-M18 key set incomplete")
    require(all(bool(coverage[k]) for k in expected), "M01-M18 contains unclosed member")
    require(coverage == successor.get("m01_m18_coverage"), "M01-M18 sidecar/receipt mismatch")
    return json.loads(canonical_json(coverage))

def validate_extension(receipt: Mapping[str, Any], scan: Mapping[str, Any]) -> dict[str, Any]:
    extension = receipt.get("extension")
    require(isinstance(extension, Mapping) and set(extension) == EXPECTED_EXTENSION_KEYS,
            "unexpected semantic extension fields")
    require(isinstance(scan, Mapping) and set(scan) == EXPECTED_SCAN_KEYS,
            "extension-scan field set mismatch")
    require(scan.get("schema") == "EE_P2R5B_F02_EXTENSION_SOURCE_REPLAY@1.0.0",
            "extension scan schema mismatch")
    require(scan.get("source_sha256") == SOURCE_SHA256, "extension scan cross-source mismatch")
    projection = extension.get("projection_material")
    expected_projection_keys = {
        "schema", "source_sha256", "accepted_base_projection_ref", "accepted_base_release_hash",
        "frozen_f02_scope_anchor", "questions", "f02_authority_refs", "negative_ceiling",
        "row_binding", "no_realization_authority_claim",
    }
    require(isinstance(projection, Mapping) and set(projection) == expected_projection_keys,
            "extension projection field set mismatch")
    require(projection.get("schema") == "EE_P2R5B_F02_I02_EXTENSION_PROJECTION@1.0.0",
            "extension projection schema mismatch")
    require(projection.get("source_sha256") == SOURCE_SHA256, "extension projection source mismatch")
    require(projection.get("accepted_base_release_hash") == BASE_RELEASE_HASH, "extension base lineage mismatch")
    require(projection.get("frozen_f02_scope_anchor") == FROZEN_SCOPE_REF, "extension scope anchor mismatch")
    require(projection.get("row_binding") == "SAME_ACCEPTED_AS2B_RESPONDENT_REFS__PHYSICAL_ROW_1BASED",
            "extension row binding changed")
    require(projection.get("no_realization_authority_claim") is True, "R5B extension claims realization authority")

    q_projection = normalized_q_members(projection.get("questions"), "extension.projection_material.questions")
    q_receipt = normalized_q_members(extension.get("question_and_member_refs"), "extension.question_and_member_refs")
    q_scan = normalized_q_members(scan.get("f02_questions"), "extension_scan.f02_questions")
    require(q_projection == q_receipt == q_scan, "q310/q311 member identity closure mismatch")

    auth_projection = normalized_f02_authorities(projection.get("f02_authority_refs"), "extension.projection_material.f02_authority_refs")
    auth_receipt = normalized_f02_authorities(extension.get("authority_refs"), "extension.authority_refs")
    auth_scan = normalized_f02_authorities(scan.get("authority_refs"), "extension_scan.authority_refs")
    require(auth_projection == auth_receipt == auth_scan, "F02 authority identity closure mismatch")

    selectors_receipt = normalized_selector_hashes(extension.get("selector_refs"))
    selectors_scan = normalized_selector_hashes(scan.get("selector_refs"))
    require(selectors_receipt == selectors_scan, "selector identity mismatch between receipt and scan")

    require(extension.get("event_count") == 58004 and extension.get("routing_count") == 58004,
            "q310/q311 extension structural cardinality mismatch")
    require(scan.get("extension_event_count") == 58004 and scan.get("extension_routing_count") == 58004,
            "q310/q311 extension scan structural cardinality mismatch")
    event_root = require_sha(scan.get("extension_event_ref_root_sha256"), "extension event root")
    routing_root = require_sha(scan.get("extension_routing_ref_root_sha256"), "extension routing root")

    qbinding = extension.get("question_binding_refs")
    require(isinstance(qbinding, Mapping) and len(qbinding) == 2, "exactly two q310/q311 question bindings required")
    qbinding_refs = {k: require_exact_ref(v, f"question_binding_refs.{k}") for k, v in qbinding.items()}
    question_ids = {
        q_projection[q]["question_ref"]["object_id"] for q in ("q310", "q311")
    }
    require(set(qbinding_refs) == question_ids, "question-binding keys must be exact q310/q311 native question IDs")
    return {
        "questions": q_projection,
        "f02_authority_refs": auth_projection,
        "selector_hashes": selectors_receipt,
        "question_binding_refs": qbinding_refs,
        "extension_event_ref_root_sha256": event_root,
        "extension_routing_ref_root_sha256": routing_root,
        "extension_event_count": 58004,
        "extension_routing_count": 58004,
    }

def validate_inputs(
    receipt_path: Path,
    replay_path: Path,
    m01_m18_path: Path,
    extension_scan_path: Path,
    authority_path: Path,
) -> dict[str, Any]:
    r5b = run_exact_r5b_verifier(receipt_path)
    receipt = load_json(receipt_path)
    require(receipt.get("schema") == "EE_P2R5B_SUCCESSOR_RELEASE_RECEIPT@1.0.0", "R5B receipt schema mismatch")
    require(receipt.get("source", {}).get("sha256") == SOURCE_SHA256, "cross-source realization forbidden")
    require(receipt.get("frozen_f02_scope_anchor", {}).get("content_hash") == FROZEN_SCOPE_HASH,
            "frozen F02 scope anchor mismatch")
    base = receipt.get("accepted_base_replay", {})
    require(base.get("semantic_release_hash") == BASE_RELEASE_HASH, "accepted base release lineage mismatch")
    require(base.get("replay_manifest_hash") == BASE_REPLAY_HASH, "accepted base replay lineage mismatch")

    successor = receipt.get("accepted_i02_successor", {})
    runtime_ref = require_exact_ref(successor.get("release_ref"), "accepted I02 runtime release", kind="C11LogicalRelease")
    require(runtime_ref == r5b["runtime_release_ref"], "runtime release ref differs from R5B verifier PASS")
    require(runtime_ref["content_hash"] != FROZEN_SCOPE_HASH, "runtime release must be distinct from frozen F02 anchor")
    require(successor.get("accepted") is True and successor.get("ingest_disposition") == "ACCEPTED_C11_LOGICAL_RELEASE",
            "runtime release is not accepted I02")
    require(successor.get("ingest_contract") == "PRE553_C11_INGEST@1.0.0", "wrong I02 ingest contract")
    require(successor.get("resolve_release_exact") == "PASS", "exact C11Repository resolution missing")
    require(successor.get("repository_release_count") == 1, "exact C11Repository cardinality mismatch")
    expected_repository_snapshot_identity = canonical_json([runtime_ref])
    require(successor.get("repository_snapshot_identity") == expected_repository_snapshot_identity,
            "C11Repository snapshot identity mismatch")
    require_sha(successor.get("candidate_projection_hash"), "candidate_projection_hash")
    require_sha(successor.get("source_release_manifest_hash"), "source_release_manifest_hash")

    expected_replay_name = successor.get("replay_manifest_file")
    expected_m_name = successor.get("m01_m18_file")
    expected_scan_name = receipt.get("extension", {}).get("source_scan_receipt_file")
    require(replay_path.name == expected_replay_name, "ReplayManifest sidecar filename mismatch")
    require(m01_m18_path.name == expected_m_name, "M01-M18 sidecar filename mismatch")
    require(extension_scan_path.name == expected_scan_name, "extension-scan sidecar filename mismatch")
    require(sha256_file(replay_path) == successor.get("replay_manifest_file_sha256"), "ReplayManifest sidecar hash mismatch")
    require(sha256_file(m01_m18_path) == successor.get("m01_m18_file_sha256"), "M01-M18 sidecar hash mismatch")
    require(sha256_file(extension_scan_path) == receipt.get("extension", {}).get("source_scan_receipt_sha256"),
            "extension-scan sidecar hash mismatch")

    replay = validate_replay_manifest(replay_path, successor)
    coverage = validate_m01_m18(m01_m18_path, successor)
    scan = load_json(extension_scan_path)
    extension = validate_extension(receipt, scan)

    boundary = receipt.get("r5a_boundary", {})
    require(boundary.get("realization_authority_claimed") is False, "R5B made realization-authority claim")
    require(boundary.get("scope_anchor_runtime_release_equality_claimed") is False, "R5B made equality claim")
    require(boundary.get("release_alias_claimed") is False, "R5B made alias claim")
    require(boundary.get("realization_binding_emitted") is False, "R5B emitted realization binding")
    require(boundary.get("facts_emitted_for_future_binding_only") is True, "R5B future-binding boundary absent")

    authority = validate_authority_material(load_json(authority_path))
    return {
        "receipt": receipt,
        "r5b_verifier_pass": r5b,
        "runtime_ref": runtime_ref,
        "successor": successor,
        "replay": replay,
        "coverage": coverage,
        "extension_scan": scan,
        "extension": extension,
        "authority": authority,
    }

def construct_binding_candidate(validated: Mapping[str, Any]) -> dict[str, Any]:
    successor = validated["successor"]
    runtime_ref = validated["runtime_ref"]
    authority = validated["authority"]
    inventory = authority["active_binding_inventory"]
    extension = validated["extension"]

    repository_resolution = {
        "operation": "C11Repository.resolve_release_exact",
        "resolution_mode": "EXACT",
        "result": "PASS",
        "runtime_release_ref": runtime_ref,
        "repository_release_count": successor["repository_release_count"],
        "repository_snapshot_identity": successor["repository_snapshot_identity"],
    }
    extension_identity_set = {
        "f02_extension_refs": extension["questions"],
        "selector_hashes": extension["selector_hashes"],
        "f02_authority_refs": extension["f02_authority_refs"],
        "question_binding_refs": extension["question_binding_refs"],
        "extension_event_ref_root_sha256": extension["extension_event_ref_root_sha256"],
        "extension_routing_ref_root_sha256": extension["extension_routing_ref_root_sha256"],
        "extension_event_count": extension["extension_event_count"],
        "extension_routing_count": extension["extension_routing_count"],
    }
    extension_identity_set_hash = sha256_obj(extension_identity_set)
    proof_closure = {
        "r5b_return_head": R5B_RETURN_HEAD,
        "r5b_verifier_git_blob_sha1": R5B_VERIFIER_GIT_BLOB_SHA1,
        "r5b_verifier_pass": True,
        "source_sha256": SOURCE_SHA256,
        "accepted_base_release_ref": BASE_RELEASE_REF,
        "accepted_base_replay_manifest_hash": BASE_REPLAY_HASH,
        "runtime_candidate_projection_hash": successor["candidate_projection_hash"],
        "runtime_source_release_manifest_hash": successor["source_release_manifest_hash"],
        "runtime_replay_manifest_ref": successor["replay_manifest_ref"],
        "runtime_replay_manifest_file_sha256": successor["replay_manifest_file_sha256"],
        "runtime_m01_m18_file_sha256": successor["m01_m18_file_sha256"],
        "runtime_m01_m18_closure_hash": sha256_obj(validated["coverage"]),
        "repository_resolution": repository_resolution,
        "extension_identity_set_hash": extension_identity_set_hash,
        "r4a_authority_hashes": R4A_AUTHORITY_HASHES,
        "r4a_successor_clause_ref": R4A_SUCCESSOR_CLAUSE_REF,
        "r5a_aggregate_ref": R5A_AGGREGATE_REF,
        "active_binding_inventory_material_hash": inventory["inventory_material_hash"],
        "active_binding_inventory_source_ref": inventory["inventory_source_ref"],
    }
    identity_material = {
        "schema_id": "RELEASE_REALIZATION_BINDING@1.0.0",
        "relation_authority_ref": RELATION_AUTHORITY_REF,
        "binding_schema_ref": BINDING_SCHEMA_REF,
        "authority_epoch_id": AUTHORITY_EPOCH_ID,
        "direction": "FROZEN_F02_SCOPE_ANCHOR_TO_ACCEPTED_PUBLIC_I02_RUNTIME_RELEASE",
        "relation_semantics": "REALIZATION__NOT_IDENTITY_EQUALITY_ALIAS_OR_BIDIRECTIONAL_SUCCESSION",
        "frozen_scope_anchor_ref": FROZEN_SCOPE_REF,
        "runtime_i02_release_ref": runtime_ref,
        "source_sha256": SOURCE_SHA256,
        "accepted_base_i02_release_ref": BASE_RELEASE_REF,
        "candidate_projection_identity": successor["candidate_projection_hash"],
        "replay_manifest_ref": successor["replay_manifest_ref"],
        "m01_m18_closure_identity": proof_closure["runtime_m01_m18_closure_hash"],
        "repository_resolution_evidence": repository_resolution,
        "extension_member_identity_set_hash": extension_identity_set_hash,
        "r4a_authority_closure_hash": R4A_AGGREGATE_HASH,
        "r4a_successor_clause_ref": R4A_SUCCESSOR_CLAUSE_REF,
        "r5a_aggregate_ref": R5A_AGGREGATE_REF,
        "uniqueness_key": uniqueness_key(),
        "authority_epoch_status": "PRE_BINDING__ZERO_ACTIVE_POSITIVE_BINDINGS_VERIFIED",
        "issuance_guard": authority["issuance_guard"],
    }
    binding_hash = sha256_obj(identity_material)
    binding_ref = {
        "kind": "ReleaseRealizationBindingCandidate@1.0.0",
        "object_id": f"urn:rawlsing:prev3:p2r6b:release-realization-binding:sha256:{binding_hash}",
        "content_hash": binding_hash,
    }
    return {
        "schema": "EE_P2R6B_RELEASE_REALIZATION_BINDING_CANDIDATE@1.0.0",
        "status": "CANDIDATE__HQ_ADOPTION_REQUIRED__NOT_ACTIVE_UNTIL_ADOPTED",
        "binding_ref": binding_ref,
        "identity_law": "SHA256_CANONICAL(identity_material)",
        "identity_material": identity_material,
        "proof_closure": proof_closure,
        "extension_identity_set": extension_identity_set,
        "semantic_boundary": {
            "directional_realization_only": True,
            "identity_equality_claimed": False,
            "alias_claimed": False,
            "reverse_inference_authorized": False,
            "selector_ast_mutated": False,
            "selector_truth_conditions_mutated": False,
            "post_outcome_mutation": False,
        },
        "activation": "HQ_ADOPTION_REQUIRED__ISSUER_OUTPUT_ALONE_IS_NOT_ACTIVE_AUTHORITY",
    }

def issue_binding_candidate(
    receipt_path: Path,
    replay_path: Path,
    m01_m18_path: Path,
    extension_scan_path: Path,
    authority_path: Path,
) -> dict[str, Any]:
    validated = validate_inputs(receipt_path, replay_path, m01_m18_path, extension_scan_path, authority_path)
    return construct_binding_candidate(validated)

FIXTURE_MARKER = "NONEMPIRICAL__NONBINDING__STRUCTURAL_FIXTURE"

def build_nonbinding_structural_fixture_candidate(*, active_binding_count: int = 0) -> dict[str, Any]:
    """Exercise deterministic mechanics without accepting or imitating an I02 release."""
    require(isinstance(active_binding_count, int) and active_binding_count >= 0, "fixture active binding count invalid")
    if active_binding_count != 0:
        raise IssuerError("fixture uniqueness court rejects nonzero active binding count")
    material = {
        "fixture_marker": FIXTURE_MARKER,
        "authority_epoch_id": AUTHORITY_EPOCH_ID,
        "direction": "FROZEN_SCOPE_MARKER_TO_RUNTIME_MARKER",
        "frozen_scope_marker": FIXTURE_MARKER + "__FROZEN_SCOPE",
        "runtime_release_marker": FIXTURE_MARKER + "__RUNTIME_RELEASE",
        "uniqueness_key": uniqueness_key(),
        "active_binding_count": active_binding_count,
        "empirical_data_present": False,
        "binding_authority_present": False,
    }
    digest = sha256_obj(material)
    return {
        "schema": "EE_P2R6B_NONEMPIRICAL_NONBINDING_STRUCTURAL_FIXTURE_CANDIDATE@1.0.0",
        "status": FIXTURE_MARKER,
        "fixture_ref": {
            "kind": "NonbindingStructuralFixture",
            "object_id": f"urn:rawlsing:prev3:p2r6b:fixture:sha256:{digest}",
            "content_hash": digest,
        },
        "identity_material": material,
        "actual_release_realization_binding": False,
        "eligible_for_hq_adoption_as_binding": False,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--replay-manifest", type=Path)
    parser.add_argument("--m01-m18", type=Path)
    parser.add_argument("--extension-scan", type=Path)
    parser.add_argument("--authority-material", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--structural-fixture", action="store_true")
    args = parser.parse_args()

    if args.structural_fixture:
        fixture = build_nonbinding_structural_fixture_candidate()
        print(json.dumps(fixture, sort_keys=True))
        return 0

    required = {
        "receipt": args.receipt,
        "replay_manifest": args.replay_manifest,
        "m01_m18": args.m01_m18,
        "extension_scan": args.extension_scan,
        "authority_material": args.authority_material,
        "output": args.output,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        parser.error("missing production inputs: " + ", ".join(missing))

    candidate = issue_binding_candidate(
        args.receipt, args.replay_manifest, args.m01_m18, args.extension_scan, args.authority_material
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "candidate": str(args.output),
        "binding_ref": candidate["binding_ref"],
        "activation": candidate["activation"],
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IssuerError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
