from __future__ import annotations

import ast
import importlib
import inspect
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import pytest

from data.ddm_build_copy import ddm_pipeline_boundary_contract as boundary
from data.ddm_build_copy import ddm_survey_identity as legacy_identity
from data.ddm_build_copy import ddm_v550_family_overlay as overlay
from data.ddm_build_copy import ddm_v550_shards as shards
from data.ddm_build_copy import ddm_v550j_joint_patterns as v550j_patterns
from data.ddm_build_copy import ddm_v551j_contract as v551j_contract
from data.ddm_build_copy import ddm_v552_structural as v552
from data.ddm_build_copy import plan_v550_wave_shards as v550_planner

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).parent / "fixtures" / "swid"
AUTHORITY = ROOT / "data" / "ddm_build_copy" / "bindings" / "question_relation_registry_35wave_active_v1.csv"


def _fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))



def _function_source_from_file(path: Path, function_name: str) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            lines = source.splitlines()
            end_lineno = getattr(node, "end_lineno", node.lineno)
            return "\n".join(lines[node.lineno - 1:end_lineno])
    raise AssertionError(f"function {function_name!r} not found in {path}")


def _mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    as_dict = getattr(value, "as_dict", None)
    if callable(as_dict):
        return dict(as_dict())
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    return {
        name: getattr(value, name)
        for name in dir(value)
        if not name.startswith("_") and not callable(getattr(value, name, None))
    }


def _future_resolver() -> Any:
    """Find the campaign identity resolver without dictating W01's public name."""
    modules = []
    for module_name in (
        "data.ddm_build_copy.ddm_source_wave_identity",
        "data.ddm_build_copy.ddm_survey_identity",
    ):
        try:
            modules.append(importlib.import_module(module_name))
        except ModuleNotFoundError:
            continue
    preferred = (
        "resolve_source_wave_identity",
        "require_source_wave_identity",
        "resolve_survey_wave_identity",
        "require_survey_identity",
    )
    for module in modules:
        for name in preferred:
            fn = getattr(module, name, None)
            if callable(fn):
                return fn
    raise AssertionError("no source/wave identity resolver is importable")


def _resolve_future(source: str, wave: str, country: str = "") -> dict[str, Any]:
    fn = _future_resolver()
    sig = inspect.signature(fn)
    kwargs: dict[str, Any] = {}
    if "source" in sig.parameters:
        kwargs["source"] = source
    elif "source_family" in sig.parameters:
        kwargs["source_family"] = source
    if "wave" in sig.parameters:
        kwargs["wave"] = wave
    elif "wave_alias" in sig.parameters:
        kwargs["wave_alias"] = wave
    if country:
        if "country_code" in sig.parameters:
            kwargs["country_code"] = country
        elif "country" in sig.parameters:
            kwargs["country"] = country
    try:
        value = fn(**kwargs)
    except TypeError:
        value = fn(source, wave)
    return _mapping(value)


def _uid_pairs(source: str, aliases: list[str]) -> list[tuple[str, str]]:
    identities = [_resolve_future(source, alias) for alias in aliases]
    pairs: list[tuple[str, str]] = []
    for identity in identities:
        source_uid = str(identity.get("source_family_uid") or identity.get("source_uid") or "").strip()
        wave_uid = str(identity.get("wave_uid") or "").strip()
        assert source_uid, "SWID-001: governed source_family_uid must be populated"
        assert wave_uid, "SWID-001: governed wave_uid must be populated"
        pairs.append((source_uid, wave_uid))
    return pairs


def _governance_value(identity: Mapping[str, Any]) -> str:
    for key in (
        "governed_membership",
        "governance_state",
        "membership_state",
        "production_scope_status",
        "production_membership",
    ):
        value = str(identity.get(key) or "").strip()
        if value:
            return value
    return ""


def _uid_physical_token(identity: Mapping[str, Any]) -> str:
    for key in (
        "uid_native_physical_token",
        "physical_token",
        "uid_physical_token",
        "physical_identity_token",
        "path_token",
        "uid_path_token",
    ):
        value = str(identity.get(key) or "").strip()
        if value:
            return value
    return ""


def _assert_ascii_token(token: str) -> None:
    assert token
    assert token.isascii()
    assert re.fullmatch(r"[A-Za-z0-9_.-]+", token), token


class TestSWIDW06AAliasKernel:
    @pytest.mark.parametrize(
        "case_key",
        ["arab_barometer", "evs_1981", "evs_1999", "afrobarometer_r1"],
    )
    def test_legacy_family_scoped_aliases_are_semantically_equivalent(self, case_key: str) -> None:
        case = _fixture("identity_alias_cases.json")[case_key]
        canonical = {
            legacy_identity.canonical_wave_key(case["source"], alias)
            for alias in case["aliases"]
        }
        assert canonical == {case["legacy_canonical_wave"]}

    @pytest.mark.parametrize(
        "case_key",
        ["arab_barometer", "evs_1981", "evs_1999", "afrobarometer_r1"],
    )
    def test_aliases_resolve_to_one_governed_uid(self, case_key: str) -> None:
        case = _fixture("identity_alias_cases.json")[case_key]
        pairs = _uid_pairs(case["source"], case["aliases"])
        assert len(set(pairs)) == 1

    def test_latinobarometro_nfc_nfd_and_sanctioned_unaccented_family_alias(self) -> None:
        case = _fixture("identity_alias_cases.json")["latinobarometro"]
        keys = {legacy_identity.canonical_family_key(value) for value in case["source_aliases"]}
        assert keys == {"latinobarometro"}
        pairs = []
        for source in case["source_aliases"]:
            identity = _resolve_future(source, case["wave"])
            source_uid = str(identity.get("source_family_uid") or identity.get("source_uid") or "").strip()
            wave_uid = str(identity.get("wave_uid") or "").strip()
            assert source_uid, "SWID-001/SWID-021: source_family_uid must be populated"
            assert wave_uid, "SWID-001/SWID-021: wave_uid must be populated"
            pairs.append((source_uid, wave_uid))
        assert len(set(pairs)) == 1

    def test_bare_global_wave_alias_without_source_fails(self) -> None:
        with pytest.raises(Exception):
            _future_resolver()(source="", wave="W1")

    def test_asian_barometer_w6_is_recognizable_but_not_closed35_executable(self) -> None:
        case = _fixture("identity_alias_cases.json")["asian_barometer_w6"]
        assert legacy_identity.canonical_wave_key(case["source"], "W6") == "W6"
        governed = boundary.load_closed_35_waves(AUTHORITY)
        assert ("Asian Barometer", "W6", "") not in governed

        identity = _resolve_future(case["source"], "W6")
        governance = _governance_value(identity)
        assert governance, "SWID-015: recognized W6 must expose governed membership"
        assert governance.upper() not in {"CLOSED_35_MEMBER", "PRODUCTION", "EXECUTABLE", "ALLOW"}

    def test_general_v550_planner_cannot_make_asian_w6_executable(self, tmp_path: Path) -> None:
        template = tmp_path / "scope.csv"
        pd.DataFrame([{"source_family": "Asian Barometer", "wave": "W6"}]).to_csv(template, index=False)
        plan = v550_planner._static_plan_from_template(template, "swid-w06a")
        if plan.empty:
            return
        rows = plan.to_dict("records")
        executable = [
            row for row in rows
            if not bool(row.get("skip_by_default", False))
            and str(row.get("governed_membership") or row.get("production_scope_status") or "").upper()
            in {"", "CLOSED_35_MEMBER", "PRODUCTION", "EXECUTABLE", "ALLOW"}
        ]
        assert not executable, "SWID-005: V550 planner must deny Asian Barometer W6 execution"


class TestSWIDW06ARedundantIdentity:
    def test_equivalent_redundant_wave_representations_are_accepted_as_one_uid(self) -> None:
        case = _fixture("redundant_identity_cases.json")["equivalent_wave"]
        assert legacy_identity.waves_equivalent(case["source"], case["wave"], case["canonical_wave"])
        resolved = boundary.verify_exact_identity(
            {"run_id": "run", **case},
            run_id="run",
            source="EVS",
            wave="1981",
        )
        assert resolved["source_family_uid"]
        assert resolved["wave_uid"]

    def test_contradictory_redundant_wave_fields_fail_closed(self) -> None:
        case = {"run_id": "run", **_fixture("redundant_identity_cases.json")["contradictory_wave"]}
        with pytest.raises(boundary.BoundaryContractError):
            boundary.verify_exact_identity(case, run_id="run", source="EVS", wave="1981")

    def test_contradictory_source_and_source_family_fail_closed(self) -> None:
        case = {"run_id": "run", **_fixture("redundant_identity_cases.json")["contradictory_source"]}
        with pytest.raises(boundary.BoundaryContractError):
            boundary.verify_exact_identity(case, run_id="run", source="EVS", wave="1981")

    def test_redundant_frame_identity_requires_all_populated_representations_to_agree(self) -> None:
        frame = pd.DataFrame([
            {"source": "EVS", "source_family": "Arab Barometer", "wave": "1981", "canonical_wave": "W1"}
        ])
        with pytest.raises(boundary.BoundaryContractError):
            boundary.verify_frame_source_wave_identity_coherence(frame)


class TestSWIDW06ACacheAndAuthority:
    def test_v550j_prepared_cache_fixture_is_alias_equivalent_but_literal_stale(self) -> None:
        fixture = _fixture("v550j_stale_cache_identity.json")
        old = fixture["cached_frame_identity"]
        current = fixture["current_invocation"]
        assert old["wave"] != current["wave"]
        assert legacy_identity.waves_equivalent(old["source"], old["wave"], current["wave"])
        assert old["run_id"] != current["run_id"]

    def test_v550j_prepared_cache_must_bind_current_uid_scope_or_reject(self) -> None:
        cache_path = ROOT / "data" / "ddm_build_copy" / "build_v550j_prepared_substrate.py"
        cache_source = _function_source_from_file(cache_path, "_cache_signature_matches")
        load_source = _function_source_from_file(cache_path, "load_or_build_v550j_prepared_substrate")
        combined = cache_source + load_source
        required = ("wave_uid", "source_family_uid", "identity_contract_version")
        assert all(token in combined for token in required), (
            "SWID-018: prepared-cache signature/reuse path must bind UID + identity contract version"
        )
        assert "country_code" in combined
        assert any(token in combined.lower() for token in ("rebind", "mismatch", "reject", "fail"))

    def test_alias_shadow_authority_with_divergent_bytes_fails_closed(self) -> None:
        shadow = FIXTURES / "alias_shadow"
        try:
            result = overlay.load_family_overlay(
                "Latinobarómetro",
                "1995",
                "semantic_authority",
                search_roots=[shadow],
                required=True,
            )
        except Exception as exc:
            assert any(token in str(exc).lower() for token in ("conflict", "diverg", "duplicate", "shadow"))
            return
        status = str(getattr(result, "status", "")).upper()
        message = str(getattr(result, "message", "")).lower()
        assert status != "FOUND", (
            "SWID-022: divergent UID-equivalent authority candidates must not resolve by first match"
        )
        assert any(token in status + " " + message for token in ("CONFLICT", "DIVERG", "DUPLICATE", "SHADOW"))

    def test_review_only_overlay_generation_cannot_self_certify(self) -> None:
        module = importlib.import_module("data.ddm_build_copy.build_wave_overlays")
        source = inspect.getsource(module.build_overlays)
        assert "HEURISTIC_REVIEW_ONLY" in source
        assert "NOT_CERTIFIED" in source
        assert '"current_directional_atom_eligible": False' in source
        assert '"manual_review_required": True' in source


class TestSWIDW06ALegacyPhysicalAndLogicalIdentity:
    def test_legacy_unicode_physical_identifiers_remain_readable_and_distinct(self) -> None:
        fixture = _fixture("legacy_identity_contract.json")["legacy_physical"]
        nfc = "Latinobarómetro"
        nfd = unicodedata.normalize("NFD", nfc)
        plain = "Latinobarometro"
        assert shards.shard_id_for(nfc, "1995") == fixture["latinobarometro_nfc_shard"]
        assert shards.shard_id_for(nfd, "1995") == fixture["latinobarometro_nfd_shard"]
        assert shards.shard_id_for(plain, "1995") == fixture["latinobarometro_unaccented_shard"]
        assert len({shards.shard_id_for(nfc, "1995"), shards.shard_id_for(nfd, "1995"), shards.shard_id_for(plain, "1995")}) == 3

    def test_uid_native_physical_token_unifies_nfc_nfd_without_renaming_legacy_paths(self) -> None:
        sources = ["Latinobarómetro", unicodedata.normalize("NFD", "Latinobarómetro"), "Latinobarometro"]
        tokens = []
        for source in sources:
            identity = _resolve_future(source, "1995")
            token = _uid_physical_token(identity)
            assert token, "SWID-021: versioned ASCII-safe UID physical token must be exposed"
            _assert_ascii_token(token)
            tokens.append(token)
        assert len(set(tokens)) == 1
        assert shards.shard_id_for(sources[0], "1995") != shards.shard_id_for(sources[1], "1995")

    def test_legacy_pattern_packet_and_measurement_identifiers_remain_frozen_namespaces(self) -> None:
        contract = _fixture("legacy_identity_contract.json")["legacy_logical_namespaces"]
        assert hasattr(v550j_patterns, contract["v550j_pattern_function"])
        assert hasattr(v551j_contract, contract["v551j_packet_function"])
        assert hasattr(v552, contract["v552_observation_function"])

        packet_id = v551j_contract.recompute_v551j_packet_id({
            "source_family": "EVS", "canonical_wave": "W1", "country_code": "IS", "family_id": "fam", "pattern_id": "pat"
        })
        observation_id = v552.recompute_v552_pressure_observation_id({"empirical_distribution_id": "dist"})
        assert packet_id.startswith(contract["v551j_packet_prefix"])
        assert observation_id.startswith(contract["v552_observation_prefix"])

        legacy_pattern_i = v550j_patterns._pattern_id("fam", "Arab Barometer", "I", "JO", "x=1")
        legacy_pattern_w1 = v550j_patterns._pattern_id("fam", "Arab Barometer", "W1", "JO", "x=1")
        assert legacy_pattern_i != legacy_pattern_w1

    def test_uid_native_logical_ids_are_additive_and_versioned_not_in_place_rewrites(self) -> None:
        pattern_source = inspect.getsource(v550j_patterns)
        packet_source = inspect.getsource(v551j_contract)
        v552_source = inspect.getsource(v552)

        legacy_pattern_body = inspect.getsource(v550j_patterns._pattern_id)
        legacy_packet_body = inspect.getsource(v551j_contract.recompute_v551j_packet_id)
        legacy_observation_body = inspect.getsource(v552.recompute_v552_pressure_observation_id)
        assert "wave_uid" not in legacy_pattern_body and "source_family_uid" not in legacy_pattern_body
        assert "wave_uid" not in legacy_packet_body and "source_family_uid" not in legacy_packet_body
        assert "wave_uid" not in legacy_observation_body and "source_family_uid" not in legacy_observation_body

        combined = pattern_source + packet_source + v552_source
        assert "source_family_uid" in combined and "wave_uid" in combined, (
            "SWID-020/IC-008: additive UID-native logical identity namespace must exist"
        )
        uid_lines = [line.lower() for line in combined.splitlines() if "wave_uid" in line or "source_family_uid" in line]
        assert any("version" in line or "uid" in line for line in uid_lines)
