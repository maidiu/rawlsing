from __future__ import annotations

import ast
from decimal import Decimal
import json
from pathlib import Path
import subprocess

import pytest

import rawlsing_next.closed35_representation_census_harness as h
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


REPO = Path(__file__).resolve().parents[2]
RETURN_DIR = REPO / "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1"
REGISTRY = RETURN_DIR / "01_CLOSED35_CENSUS_INPUT_REGISTRY.json"
SURFACES = RETURN_DIR / "03_GOVERNED_TYPED_SURFACE_REGISTRY.csv"
RUNNER = RETURN_DIR / "02_RUN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS.sh"
HARNESS = REPO / "rawlsing_next/closed35_representation_census_harness.py"
R5 = R5TypedValueCodec()


def test_exact_35_source_registry_is_frozen_and_valid():
    registry = h.load_source_registry(REGISTRY)
    assert registry["source_count"] == 35
    assert registry["sav_count"] == 31
    assert registry["dta_count"] == 4
    assert [x["source_id"] for x in registry["sources"]] == [f"{i:02d}" for i in range(1, 36)]
    assert all(len(x["canonical_sha256"]) == 64 for x in registry["sources"])


def test_all_decoder_lanes_resolve_without_opening_sources():
    registry = h.load_source_registry(REGISTRY)
    lanes = [h.resolve_decoder_lane(x) for x in registry["sources"]]
    assert len(lanes) == 35
    assert all(x["reader"] in {"pyreadstat.read_sav", "pyreadstat.read_dta"} for x in lanes)


def test_declared_encoding_admission_gaps_are_explicit_not_guessed():
    registry = h.load_source_registry(REGISTRY)
    by_id = {x["source_id"]: x for x in registry["sources"]}
    assert h.resolve_decoder_lane(by_id["08"])["generic_debt"] == "GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP"
    assert h.resolve_decoder_lane(by_id["08"])["encoding"] == "BIG5"
    for sid in ("11", "12"):
        lane = h.resolve_decoder_lane(by_id[sid])
        assert lane["generic_debt"] == "GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP"
        assert lane["encoding"] == "WINDOWS-1252"


def test_surface_registry_count_and_owner_partition_are_explicit():
    surfaces = h.load_surface_registry(SURFACES)
    assert len(surfaces) == 38
    assert sum(x["owner_key_status"] == "MISSING_EXACT_VALUE_KEY_AUTHORITY" for x in surfaces) == 20
    assert sum(x["owner_key_status"] != "MISSING_EXACT_VALUE_KEY_AUTHORITY" for x in surfaces) == 18


def test_known_commission_surfaces_are_present():
    surfaces = h.load_surface_registry(SURFACES)
    pairs = {(x["source_file"], x["variable_name"]) for x in surfaces}
    required = {
        ("LiTS_I.dta", "q301_2"),
        ("LiTS_I.dta", "q301_7"),
        ("WVS Wave 7.sav", "Q291G5"),
        ("WVS Wave 7.sav", "Q291P5"),
        ("Latinobarometro 1995.sav", "p27e"),
        ("Latinobarometro 1995.sav", "p27g"),
        ("Latinobarometro 1995.sav", "p27m"),
        ("South Asia Wave 1.sav", "c13f"),
        ("South Asia Wave 1.sav", "c13h"),
        ("Afro Barometer Round 5.sav", "Q10B"),
        ("Afro Barometer Round 9.sav", "Q78F"),
        ("Afro Barometer Round 9.sav", "Q47C"),
        ("Afro Barometer Round 9.sav", "Q118"),
    }
    assert required <= pairs
    for name in ("abdefect", "abhlth", "abrape", "abany", "absingle", "abnomore"):
        assert ("GSS2010.sav", name) in pairs
    for pair in (("Arab Barometer Wave 2.sav", "Q101"), ("Arab Barometer Wave 2.sav", "Q2062"),
                 ("Arab Barometer Wave 5.sav", "Q101"), ("Arab Barometer Wave 5.sav", "Q2061B")):
        assert pair in pairs


def test_surface_registry_source_id_sha_join_is_exact():
    registry = h.load_source_registry(REGISTRY)
    surfaces = h.load_surface_registry(SURFACES)
    by_id = {x["source_id"]: x for x in registry["sources"]}
    for surface in surfaces:
        source = by_id[surface["source_id"]]
        assert surface["source_file"] == source["canonical_filename"]
        assert surface["source_sha256"] == source["canonical_sha256"]


@pytest.mark.parametrize("classification_name", h.CLASSIFICATIONS)
def test_every_classification_enum_is_reachable(classification_name):
    assert h.classification(classification_name) == classification_name


def test_classification_law_hits_all_non_source_unavailable_paths():
    assert h.classify_surface(
        owner_key_status="NATIVE_LITERAL_RULE_OWNER",
        representation_authority="",
        exact_join=True,
        observed_physical_types=["int"],
        rule_native_python_type="int",
    ) == "EXACT_EXISTING_REGIME_APPLIES"
    assert h.classify_surface(
        owner_key_status="EXACT_BOUNDED_OWNER",
        representation_authority="FIABC-LITS-I-Q301-DTA-DECODER-REPRESENTATION-REPLAY@1.0.0",
        exact_join=False,
        observed_physical_types=["float"],
        rule_native_python_type="int",
        bounded_bridge_pass=True,
    ) == "EXACT_BOUNDED_SUCCESSOR_BRIDGE_APPLIES"
    assert h.classify_surface(
        owner_key_status="NATIVE_LITERAL_RULE_OWNER",
        representation_authority="",
        exact_join=False,
        observed_physical_types=["float"],
        rule_native_python_type="int",
    ) == "NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED"
    assert h.classify_surface(
        owner_key_status="NATIVE_LITERAL_RULE_OWNER",
        representation_authority="",
        exact_join=False,
        observed_physical_types=["str"],
        rule_native_python_type="int",
    ) == "SOURCE_BOUNDED_REPRESENTATION_BRIDGE_REQUIRED"
    assert h.classify_surface(
        owner_key_status="MISSING_EXACT_VALUE_KEY_AUTHORITY",
        representation_authority="",
        exact_join=False,
        observed_physical_types=["float"],
        rule_native_python_type="",
    ) == "TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY"


def test_runtime_gate_is_exact_and_rejects_nearby_versions():
    h.validate_runtime_facts(h.EXPECTED_RUNTIME)
    bad = dict(h.EXPECTED_RUNTIME)
    bad["cpython"] = "3.11.4"
    with pytest.raises(h.GlobalIntegrityError, match="RUNTIME_GATE_FAILED"):
        h.validate_runtime_facts(bad)
    bad = dict(h.EXPECTED_RUNTIME)
    bad["machine"] = "arm64"
    with pytest.raises(h.GlobalIntegrityError, match="RUNTIME_GATE_FAILED"):
        h.validate_runtime_facts(bad)


def test_int_float_decimal_and_decimal_exponent_do_not_collapse_in_r5():
    assert R5.encode(1) != R5.encode(1.0)
    assert R5.encode(1) != R5.encode(Decimal("1"))
    assert R5.encode(1.0) != R5.encode(Decimal("1.0"))
    assert R5.encode(Decimal("1")) != R5.encode(Decimal("1.0"))


def test_physical_binding_key_preserves_typed_numeric_noncollapse():
    state = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    keys = {
        physical_value_binding_key(1, state),
        physical_value_binding_key(1.0, state),
        physical_value_binding_key(Decimal("1"), state),
        physical_value_binding_key(Decimal("1.0"), state),
    }
    assert len(keys) == 4


def test_missing_state_and_source_declaration_do_not_collapse():
    observed = physical_value_binding_key(997.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None)
    user = physical_value_binding_key(
        997.0,
        PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
        {"kind": "discrete", "value": 997.0},
    )
    user_other_declaration = physical_value_binding_key(
        997.0,
        PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
        {"kind": "discrete", "value": 998.0},
    )
    system = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
    assert len({observed, user, user_other_declaration, system}) == 4


def test_string_bytes_and_blank_string_lanes_are_exact():
    assert R5.encode("") == {"t": "str", "v": ""}
    assert R5.encode(b"") == {"t": "bytes", "b64": ""}
    assert R5.encode("") != R5.encode(b"")
    assert R5.encode("0") != R5.encode(0)


def test_synthetic_latin2024_raw_header_keeps_174_separate_from_normalized_332():
    prefix = bytearray(176)
    prefix[0:4] = b"$FL2"
    prefix[64:68] = (2).to_bytes(4, "little", signed=True)
    prefix[68:72] = (174).to_bytes(4, "little", signed=True)
    prefix[72:76] = (1).to_bytes(4, "little", signed=True)
    prefix[76:80] = (0).to_bytes(4, "little", signed=True)
    prefix[80:84] = (19214).to_bytes(4, "little", signed=True)
    parsed = h._sav_header_layout(bytes(prefix))
    assert parsed["nominal_case_size"] == 174
    synthetic_metadata = {"raw_sav_fixed_header": parsed, "logical_variable_count": 332}
    registry = h.load_source_registry(REGISTRY)
    source = {x["source_id"]: x for x in registry["sources"]}["26"]
    edge = h._edge_receipt_for_source(source, synthetic_metadata)
    witness = edge["special_witnesses"]["latinobarometro_2024_raw_header_vs_stream"]
    assert witness == {
        "raw_nominal_case_size": 174,
        "normalized_dictionary_stream_width": 332,
        "expected": [174, 332],
        "pass": True,
    }
    assert "GENERIC_RAW_HEADER_METADATA_CARRIER_GAP" not in edge["generic_debts"]


def test_latin2024_generic_gap_is_emitted_if_either_witness_disappears():
    registry = h.load_source_registry(REGISTRY)
    source = {x["source_id"]: x for x in registry["sources"]}["26"]
    edge = h._edge_receipt_for_source(
        source,
        {"raw_sav_fixed_header": {"nominal_case_size": None}, "logical_variable_count": 332},
    )
    assert "GENERIC_RAW_HEADER_METADATA_CARRIER_GAP" in edge["generic_debts"]


def test_path_manifest_is_source_id_driven_and_does_not_infer_filenames():
    manifest = {
        "schema": h.PATH_MANIFEST_SCHEMA,
        "sources": {"01": "/arbitrary/opaque/carrier.bin", "35": "/other/path/no-name-match"},
    }
    parsed = h.validate_path_manifest(manifest)
    assert parsed["01"].endswith("carrier.bin")
    assert parsed["35"].endswith("no-name-match")
    with pytest.raises(h.GlobalIntegrityError):
        h.validate_path_manifest({"schema": h.PATH_MANIFEST_SCHEMA, "sources": {"99": "/x"}})


def test_historical_dependency_origins_reject_ambient_current_leak():
    records = list(h.dependency_provenance_records())
    h.audit_dependency_origins(records)
    records.append({"dependency": "bad", "origin": "ACCIDENTAL_CURRENT_DEPENDENCY_LEAK"})
    with pytest.raises(h.GlobalIntegrityError, match="accidental current dependency leak"):
        h.audit_dependency_origins(records)


def test_historical_dependency_blob_pins_are_exactly_recoverable():
    receipt = h.build_dependency_receipt(REPO)
    assert receipt["pass"] is True
    assert receipt["ambient_current_dependency_leaks"] == []
    by_name = {x["dependency"]: x for x in receipt["records"]}
    assert by_name["lits_legacy_facade"]["verified_blob"] == "7c509c2098d0030f253344eb3f682471378812a8"
    assert by_name["lits_legacy_canonicalize_semantic_hash"]["verified_blob"] == "a61365b994e5c3c50de0f598fcf40e90abf757b6"
    assert by_name["lits_legacy_missing_state_enum"]["verified_blob"] == "13aa733b511dc23e00bfcdf288c5b920e3f09983"



def test_every_surface_authority_locator_resolves_or_is_exact_historical_pin():
    surfaces = h.load_surface_registry(SURFACES)
    for surface in surfaces:
        locator = surface["authority_locator"]
        if ":" in locator and locator.split(":", 1)[0].isalnum() and len(locator.split(":", 1)[0]) == 40:
            commit, authority_path = locator.split(":", 1)
            result = subprocess.run(
                ["git", "-C", str(REPO), "cat-file", "-e", f"{commit}:{authority_path}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            assert result.returncode == 0, locator
        else:
            assert (REPO / locator).is_file(), locator


def test_current_decoder_exposes_raw_header_and_normalized_geometry_separately():
    source = (REPO / "rawlsing_next/pre553_physical_decoder.py").read_text(encoding="utf-8")
    assert '"raw_layout_declarations"' in source
    assert '"normalized_geometry"' in source
    assert '"nominal_case_size"' in source
    assert "automatic encoding guessing/fallback is forbidden" in source

def test_source_receipt_schema_accepts_only_pass_or_blocked():
    receipt = {
        "schema": h.SOURCE_RECEIPT_SCHEMA,
        "status": "PASS",
        "surfaces": [{"classification": "EXACT_EXISTING_REGIME_APPLIES"}],
    }
    h.validate_source_receipt(receipt)
    with pytest.raises(h.CensusError):
        h.validate_source_receipt({**receipt, "status": "MAYBE"})


def test_immutable_receipt_same_bytes_resume_and_drift_fails(tmp_path):
    path = tmp_path / "SOURCE_01_REPRESENTATION_RECEIPT.json"
    payload = {"a": 1}
    assert h.immutable_json(path, payload) == "CREATED"
    assert h.immutable_json(path, payload) == "RESUMED_IDENTICAL"
    with pytest.raises(h.GlobalIntegrityError, match="immutable receipt drift"):
        h.immutable_json(path, {"a": 2})


def _fake_registry():
    sources = []
    for i in range(1, 36):
        sources.append({
            "source_id": f"{i:02d}",
            "canonical_filename": f"S{i:02d}.sav",
            "canonical_sha256": f"{i:064x}"[-64:],
            "edge_classes": ["EC01"],
            "documentary_unknowns": "UNKNOWN",
        })
    return {"sources": sources}


def _fake_receipt(source, runtime, manifest_hash, status="PASS", blocker=None):
    value = {
        "schema": h.SOURCE_RECEIPT_SCHEMA,
        "contract": h.CONTRACT,
        "source_id": source["source_id"],
        "source_file": source["canonical_filename"],
        "canonical_sha256": source["canonical_sha256"],
        "status": status,
        "runtime": runtime,
        "path_manifest_sha256": manifest_hash,
        "surfaces": [],
        "edge_preservation": {
            "edge_classes": source["edge_classes"],
            "documentary_unknowns_preserved": source["documentary_unknowns"],
            "semantic_interpretation_authorized": False,
        },
    }
    if blocker:
        value["blocker"] = blocker
    return value


def test_one_source_failure_preserves_prior_receipts_and_later_sources_continue(monkeypatch, tmp_path):
    runtime = h.RuntimeFacts(**h.EXPECTED_RUNTIME)
    monkeypatch.setattr(h, "require_repository_guard", lambda *a, **k: {
        "branch": h.EXPECTED_BRANCH,
        "head": "b" * 40,
        "qualified_code_head": "a" * 40,
        "post_qualification_paths": [],
    })
    monkeypatch.setattr(h, "require_qualified_runtime", lambda: runtime)
    monkeypatch.setattr(h, "load_source_registry", lambda *a, **k: _fake_registry())
    monkeypatch.setattr(h, "load_surface_registry", lambda *a, **k: ())
    monkeypatch.setattr(h, "build_dependency_receipt", lambda *a, **k: {
        "schema": h.DEPENDENCY_RECEIPT_SCHEMA, "records": [], "ambient_current_dependency_leaks": [], "pass": True
    })

    calls = []
    def observer(*, source, source_path_text, surfaces, runtime, manifest_hash):
        calls.append(source["source_id"])
        if source["source_id"] == "23":
            raise RuntimeError("synthetic source-local failure")
        return _fake_receipt(source, runtime, manifest_hash)

    manifest = tmp_path / "paths.json"
    manifest.write_text(json.dumps({"schema": h.PATH_MANIFEST_SCHEMA, "sources": {}}))
    out = tmp_path / "out"
    assert h.run_census(
        repo_root=REPO,
        manifest_path=manifest,
        output_root=out,
        qualified_code_head="a" * 40,
        observer=observer,
    ) == 0
    assert calls == [f"{i:02d}" for i in range(1, 36)]
    for i in range(1, 36):
        assert (out / "source_receipts" / f"SOURCE_{i:02d}_REPRESENTATION_RECEIPT.json").is_file()
    blocked = json.loads((out / "source_receipts/SOURCE_23_REPRESENTATION_RECEIPT.json").read_text())
    assert blocked["status"] == "BLOCKED"
    assert "synthetic source-local failure" in blocked["blocker"]
    assert json.loads((out / "source_receipts/SOURCE_24_REPRESENTATION_RECEIPT.json").read_text())["status"] == "PASS"


def test_rerun_resume_does_not_reinvoke_completed_source_observer(monkeypatch, tmp_path):
    runtime = h.RuntimeFacts(**h.EXPECTED_RUNTIME)
    monkeypatch.setattr(h, "require_repository_guard", lambda *a, **k: {
        "branch": h.EXPECTED_BRANCH,
        "head": "b" * 40,
        "qualified_code_head": "a" * 40,
        "post_qualification_paths": [],
    })
    monkeypatch.setattr(h, "require_qualified_runtime", lambda: runtime)
    monkeypatch.setattr(h, "load_source_registry", lambda *a, **k: _fake_registry())
    monkeypatch.setattr(h, "load_surface_registry", lambda *a, **k: ())
    monkeypatch.setattr(h, "build_dependency_receipt", lambda *a, **k: {
        "schema": h.DEPENDENCY_RECEIPT_SCHEMA, "records": [], "ambient_current_dependency_leaks": [], "pass": True
    })
    manifest = tmp_path / "paths.json"
    manifest.write_text(json.dumps({"schema": h.PATH_MANIFEST_SCHEMA, "sources": {}}))
    out = tmp_path / "out"
    calls = []
    def first_observer(*, source, source_path_text, surfaces, runtime, manifest_hash):
        calls.append(source["source_id"])
        return _fake_receipt(source, runtime, manifest_hash)
    h.run_census(repo_root=REPO, manifest_path=manifest, output_root=out,
                 qualified_code_head="a" * 40, observer=first_observer)
    assert len(calls) == 35

    def forbidden_observer(**kwargs):
        raise AssertionError("resume must not re-observe completed sources")
    h.run_census(repo_root=REPO, manifest_path=manifest, output_root=out,
                 qualified_code_head="a" * 40, observer=forbidden_observer)


def test_source_receipt_failure_does_not_prepopulate_observation_results():
    registry = h.load_source_registry(REGISTRY)
    assert all("observed" not in json.dumps(source).lower() or "observed" in source["accepted_physical_hazards"].lower()
               for source in registry["sources"])


def test_harness_import_graph_has_no_candidate_or_measured_p2x_imports():
    tree = ast.parse(HARNESS.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    forbidden = ("candidate", "measured_p2x", "ee_p2x_candidate")
    assert not [name for name in imported if any(fragment in name.lower() for fragment in forbidden)]


def test_runner_has_no_candidate_or_measured_p2x_execution_path():
    text = RUNNER.read_text(encoding="utf-8").lower()
    assert "candidate a" not in text
    assert "candidate b" not in text
    assert "candidate c" not in text
    assert "measured_p2x" not in text
    assert "-m rawlsing_next.closed35_representation_census_harness" in text


def test_runner_runtime_gate_is_exact_and_placeholder_fail_closed_before_rebind():
    text = RUNNER.read_text(encoding="utf-8")
    for literal in ("Darwin", "x86_64", "3.11.3", "1.3.6", "25.0.1"):
        assert literal in text
    assert "__SOURCE_FREE_QUALIFIED_CODE_HEAD__" in text


def test_post_qualification_allowlist_rejects_code_drift():
    h.validate_post_qualification_paths([
        "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/00_RETURN.md"
    ])
    with pytest.raises(h.GlobalIntegrityError, match="post-qualification code/data drift"):
        h.validate_post_qualification_paths(["rawlsing_next/closed35_representation_census_harness.py"])


def test_aggregate_output_schemas_are_deterministic(tmp_path):
    runtime = {"schema": h.RUNTIME_RECEIPT_SCHEMA, "pass": True}
    dependency = {"schema": h.DEPENDENCY_RECEIPT_SCHEMA, "records": [], "pass": True}
    source = _fake_registry()["sources"][0]
    receipt = _fake_receipt(source, h.EXPECTED_RUNTIME, "0" * 64)
    h.build_aggregate_outputs([receipt], runtime, dependency, tmp_path)
    assert json.loads((tmp_path / "CLOSED35_REPRESENTATION_OBSERVATIONS.json").read_text())["schema"] == h.OBSERVATIONS_SCHEMA
    assert json.loads((tmp_path / "CLOSED35_EDGE_PRESERVATION_RECEIPT.json").read_text())["schema"] == h.EDGE_RECEIPT_SCHEMA
    assert json.loads((tmp_path / "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json").read_text())["schema"] == h.DEPENDENCY_RECEIPT_SCHEMA
    assert json.loads((tmp_path / "CLOSED35_RUNTIME_RECEIPT.json").read_text())["schema"] == h.RUNTIME_RECEIPT_SCHEMA
    assert json.loads((tmp_path / "CLOSED35_CENSUS_SUMMARY.json").read_text())["schema"] == h.SUMMARY_SCHEMA
    first = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    h.build_aggregate_outputs([receipt], runtime, dependency, tmp_path)
    assert first == {p.name: p.read_bytes() for p in tmp_path.iterdir()}
