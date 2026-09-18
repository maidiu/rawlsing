from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

import rawlsing_next.pre553_c11_ingest as ingest
import rawlsing_next.pre553_c11_repository as repo_mod
import rawlsing_next.pre553_carrier_execution as carrier
from rawlsing_next.pre553_c11_integrity import C11AtomicityError
from rawlsing_next.pre553_empirical_objects import ExactRef

ROOT = Path(__file__).resolve().parents[2]
RET = ROOT / "WORKER_RETURNS" / "EE-P2R4B"
F02_HASH = "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
BASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
SOURCE_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"

def load(name: str):
    return json.loads((RET / name).read_text(encoding="utf-8"))

def test_frozen_identity_map_is_exact_and_six_selectors_are_not_reminted():
    x = load("02_F02_COMPOSITE_RELEASE_MEMBER_AND_IDENTITY_MAP.json")
    assert x["source_sha256"] == SOURCE_SHA
    assert x["base_release_ref"]["content_hash"] == BASE_HASH
    assert x["frozen_composite_release_ref"]["content_hash"] == F02_HASH
    assert x["identity_material_schema"] == "F02_LITS1_C11_COMPOSITE_RELEASE@1.0.0"
    selectors = x["exact_extension"]["selectors"]
    assert len(selectors) == 6
    assert set(selectors.values()) == {
        "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
        "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
        "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
        "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
        "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
        "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
    }

def test_current_i02_semantic_release_hash_is_not_caller_supplied():
    src = inspect.getsource(ingest.validate_c11_source_release)
    assert 'projection_hash = semantic_hash({' in src
    assert '"candidate_projection_hash": replay_manifest.semantic_projection_hash' in src
    assert '"replay_manifest_ref": replay_manifest.ref.as_dict()' in src
    assert '"m01_m18": {k: list(v) for k, v in coverage.items()}' in src
    assert "semantic_release_hash=projection_hash" in src
    assert "semantic_release_hash=F02_HASH" not in src

def test_i02_replay_is_full_candidate_closure_not_f02_reference_union():
    replay_src = inspect.getsource(ingest.build_candidate_replay_manifest)
    assert "_candidate_projection_semantic_hash(candidate)" in replay_src
    assert "_all_nonmanifest_refs(candidate)" in replay_src
    compat = load("03_I02_COMPOSITE_REALIZATION_COMPATIBILITY.json")
    assert compat["comparison"]["f02"]["hash_law"] != compat["comparison"]["i02"]["release_hash_law"]
    assert compat["compatibility"]["lossless_release_ref_map_possible"] is False

def test_public_repository_rejects_unvalidated_release_construction():
    source_ref = ExactRef("SOURCE_ARTIFACT", "urn:test:source", SOURCE_SHA)
    with pytest.raises(C11AtomicityError, match="complete I02 validation"):
        repo_mod.C11LogicalRelease(
            release_id="LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669",
            source_artifact_ref=source_ref,
            source_release_manifest_hash="1" * 64,
            semantic_release_hash=F02_HASH,
            replay_manifest=None,
            public_objects=(),
            internal_records=(),
            m01_m18_coverage={},
        )

def test_repository_commit_primitive_is_validation_seal_gated():
    src = inspect.getsource(repo_mod.C11Repository._commit_validated)
    assert "_validation_seal is not _C11_VALIDATION_SEAL" in src
    assert "repository accepts only I02-validated sealed C11LogicalRelease" in src
    receipt = load("04_C11REPOSITORY_EXACT_BINDING_RECEIPT.json")
    assert receipt["disposition"]["repository_mutated"] is False
    assert receipt["disposition"]["fail_closed"] is True

def test_p2r1_requires_exact_repository_resolution_before_executor_binding():
    src = inspect.getsource(carrier.bind_repository_builder)
    assert "isinstance(repository, C11Repository)" in src
    assert "repository.resolve_release_exact(release_ref)" in src
    assert "repository builder returned release absent from returned repository" in src
    receipt = load("05_P2R1_STRUCTURAL_BINDING_RECEIPT.json")
    assert receipt["holding"]["exact_f02_repository_pair_available"] is False
    assert receipt["holding"]["predicate_evaluation_attempted"] is False
    assert receipt["holding"]["mixed_i05_execution_attempted"] is False

def test_block_precedes_carrier_and_has_no_local_residual():
    compat = load("03_I02_COMPOSITE_REALIZATION_COMPATIBILITY.json")
    residual = load("06_LOCAL_RESIDUAL_IF_ANY.json")
    assert compat["compatibility"]["carrier_bytes_change_this_conclusion"] is False
    assert residual["local_residual"] is False
    assert residual["maximum_local_codex_intelligence_required"] == "NOT_APPLICABLE"
    assert residual["source_materialization_required_to_adjudicate_r4b"] is False
