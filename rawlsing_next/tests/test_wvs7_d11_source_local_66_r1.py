from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rawlsing_next.pre553_source_local_universe_admission import (
    CLAIM_CEILING,
    REQUIRED_NEGATIVE_LIMIT_REFS,
)

ROOT = Path(__file__).resolve().parents[2]
RETURN_DIR = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/W_WVS7_HB01_SOURCE_CERTIFICATION_R1/"
    "WORKER_RETURNS/D11_SOURCE_LOCAL_66_R1"
)
SCRIPT = RETURN_DIR / "BUILD_D11_SOURCE_LOCAL_66.py"
ARTIFACT_OUT = ROOT / ".rabochii/generated_wvs7_d11_source_local_66"
FILES = (
    "SOURCE_LOCAL_ADMISSION_AUTHORITIES.json",
    "SOURCE_LOCAL_EMPIRICAL_UNIVERSES.json",
    "SOURCE_LOCAL_66_REPLAY_PARITY_RECEIPT.json",
)


def _run(out: Path) -> subprocess.CompletedProcess[str]:
    out.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(out)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _authority_ref_key(value):
    return (
        value["authority_id"],
        value["authority_version"],
        value["authority_content_hash"],
    )


def _exact_ref_key(value):
    return (value["kind"], value["object_id"], value["content_hash"])


def test_wvs7_d11_source_local_66_two_outer_processes_exact_and_bounded():
    if ARTIFACT_OUT.exists():
        shutil.rmtree(ARTIFACT_OUT)

    first = _run(ARTIFACT_OUT)
    assert first.returncode == 0, first.stderr or first.stdout

    with tempfile.TemporaryDirectory(prefix="wvs7-d11-source-local-66-outer2-") as td:
        second_dir = Path(td)
        second = _run(second_dir)
        assert second.returncode == 0, second.stderr or second.stdout

        for name in FILES:
            left = (ARTIFACT_OUT / name).read_bytes()
            right = (second_dir / name).read_bytes()
            assert left == right, f"outer-process byte drift: {name}"

    authorities = _load(ARTIFACT_OUT / FILES[0])
    universes = _load(ARTIFACT_OUT / FILES[1])
    receipt = _load(ARTIFACT_OUT / FILES[2])

    assert authorities["scope_count"] == 66
    assert universes["scope_count"] == 66
    assert universes["total_members"] == 97220
    assert receipt["scope_count"] == 66
    assert receipt["total_members"] == 97220

    authority_rows = authorities["authorities"]
    universe_rows = universes["universes"]
    assert len(authority_rows) == 66
    assert len(universe_rows) == 66

    scope_refs = [
        _exact_ref_key(row["scope"]["source_scope_member_set_ref"])
        for row in authority_rows
    ]
    assert len(scope_refs) == len(set(scope_refs)) == 66

    authority_ids = [
        _authority_ref_key(row["authority"]["semantic_fields"]["authority_id"] and {
            "authority_id": row["authority"]["semantic_fields"]["authority_id"],
            "authority_version": row["authority"]["semantic_fields"]["authority_version"],
            "authority_content_hash": row["authority"]["semantic_fields"]["authority_content_hash"],
        })
        for row in authority_rows
    ]
    assert len(authority_ids) == len(set(authority_ids)) == 66

    universe_refs = [
        (row["universe"]["object_id"], row["universe"]["content_hash"])
        for row in universe_rows
    ]
    assert len(universe_refs) == len(set(universe_refs)) == 66

    expected_negative_refs = {
        _exact_ref_key(ref.as_dict()) for ref in REQUIRED_NEGATIVE_LIMIT_REFS
    }

    for row in authority_rows:
        auth = row["authority"]
        sf = auth["semantic_fields"]
        assert auth["typed_state"] == "ALLOW"
        assert sf["decision_state"] == "ALLOW"
        assert sf["authority_kind"] == "SOURCE_SEMANTICS_TOPOLOGY"
        assert sf["governed_operations"] == [
            "SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1"
        ]
        assert sf["governed_object_families"] == ["EmpiricalUniverse@1.0.0"]
        assert sf["scope_envelope"]["claim_ceiling"] == CLAIM_CEILING
        assert sf["scope_envelope"]["default_measure_ceiling"] == "RAW_ONLY"
        assert (
            sf["scope_envelope"]["population_generalization"]
            == "DENIED_UNLESS_SEPARATELY_AUTHORIZED"
        )
        got_negative_refs = {
            _exact_ref_key(value) for value in sf["negative_limit_refs"]
        }
        assert expected_negative_refs.issubset(got_negative_refs)

    source_native_triples = set()
    for row in universe_rows:
        scope = row["scope"]
        uni = row["universe"]
        sf = uni["semantic_fields"]

        source_native_triples.add(
            (scope["S025"], scope["B_COUNTR"], scope["A_YEAR"])
        )
        assert sf["source_local_claim_ceiling"] == CLAIM_CEILING
        assert (
            sf["target_population_and_sample_frame"]["state"]
            == "NOT_POPULATION_CERTIFIED"
        )
        assert (
            sf["sampling_design_regime"]["state"]
            == "NOT_POPULATION_CERTIFIED"
        )
        assert sf["harmonization_authority_ref"] is None
        assert sf["source_relation_refs"] == []
        assert sf["canonical_wave_if_governed"] is None

        geography = sf["country_geography"]
        assert set(geography) == {
            "A_YEAR",
            "B_COUNTR",
            "S025",
            "claim_ceiling",
            "scope_key",
        }
        assert "country_name" not in geography
        assert "iso" not in geography

    assert len(source_native_triples) == 66

    assert receipt["population_generalization_permissions"] == 0
    assert receipt["weighted_population_permissions"] == 0
    assert receipt["pooling_permissions"] == 0
    assert receipt["backfill_permissions"] == 0
    assert receipt["harmonization_permissions"] == 0
    assert receipt["qualification_state"] == "SINGLE_BUILD__OUTER_PROCESS_PARITY_REQUIRED"
