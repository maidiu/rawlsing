from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RET = ROOT / "WORKER_RETURNS" / "EE-P2R5B"

EXPECTED_BLOBS = {
    RET / "SUPPORT/FROZEN_BASE/AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827/run_as2b_lits1_mechanical_certification.py":
        "c51b56779ab9d79126619b7733d41f5253c8150f",
    RET / "SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv":
        "c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c",
    RET / "SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json":
        "174b931e8aa89111086e3d46159b47154bed7f16",
    RET / "SUPPORT/FROZEN_F02/prev3_lits1_selector_closure.py":
        "7b45b277164fa90c3da739aab26b516f7a8cb8dc",
}

EXPECTED_SELECTORS = {
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:1": "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:2": "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:3": "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:1": "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:2": "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:3": "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()


def load_json(name: str):
    return json.loads((RET / name).read_text(encoding="utf-8"))


def test_frozen_support_blobs_are_exact():
    for path, expected in EXPECTED_BLOBS.items():
        assert path.is_file()
        assert git_blob_sha(path) == expected


def test_prepared_python_artifacts_parse_without_execution():
    for name in ("03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py", "05_SUCCESSOR_RELEASE_VERIFIER.py"):
        source = (RET / name).read_text(encoding="utf-8")
        ast.parse(source, filename=name)


def test_f02_frozen_producer_reconstructs_exact_scope_and_selectors_without_carrier_access():
    path = RET / "SUPPORT/FROZEN_F02/prev3_lits1_selector_closure.py"
    spec = importlib.util.spec_from_file_location("ee_p2r5b_qual_f02", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    closure = module.build_selector_closure()
    assert closure["new_release_ref"]["content_hash"] == "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
    assert closure["base_release_ref"]["content_hash"] == "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
    got = {sid: item["predicate_ref"]["content_hash"] for sid, item in closure["selectors"].items()}
    assert got == EXPECTED_SELECTORS
    assert module.QUESTION_SPECS["q310"][0] == 229
    assert module.QUESTION_SPECS["q311"][0] == 230


def test_construction_map_does_not_predeclare_successor_hash_or_authority():
    data = load_json("01_SUCCESSOR_I02_CANDIDATE_CONSTRUCTION_MAP.json")
    law = data["output_identity_law"]
    assert law["expected_successor_semantic_release_hash"] is None
    assert law["hardcode_forbidden"] is True
    assert data["r5a_boundary"]["authority_question_decided_here"] is False
    assert data["r5a_boundary"]["scope_anchor_runtime_release_equality_claimed"] is False
    assert data["r5a_boundary"]["realization_binding_emitted"] is False
    assert data["base_identity_preservation"]["strategy"] == "BUILD_ACCEPTED_BASE_CANDIDATE_FIRST__THEN_UNION_EXTENSION"


def test_receipt_schema_fails_closed_on_r5a_boundary():
    schema = load_json("04_SUCCESSOR_RELEASE_RECEIPT_SCHEMA.json")
    props = schema["properties"]["r5a_boundary"]["properties"]
    assert props["realization_authority_claimed"]["const"] is False
    assert props["scope_anchor_runtime_release_equality_claimed"]["const"] is False
    assert props["release_alias_claimed"]["const"] is False
    assert props["realization_binding_emitted"]["const"] is False


def test_local_packet_is_mechanical_and_luna_sufficient():
    packet = load_json("06_LOCAL_EXECUTION_PACKET.json")
    assert packet["maximum_local_machine_codex_intelligence_required"] == "LUNA"
    assert packet["semantic_judgment_remaining_for_local_worker"] is False
    assert packet["network_access_needed"] is False
    assert packet["expected_output_filenames"] == [
        "successor_release_receipt.json",
        "successor_release_replay_manifest.json",
        "successor_release_m01_m18.json",
        "successor_release_extension_scan.json",
    ]


def test_driver_contains_no_caller_chosen_successor_hash():
    source = (RET / "03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py").read_text(encoding="utf-8")
    assert "expected_successor_semantic_release_hash" not in source
    assert "ingest_c11_source_release(successor_candidate, repository)" in source
    assert "repository.resolve_release_exact(ingest.release_ref)" in source
    assert '"scope_anchor_runtime_release_equality_claimed": False' in source
