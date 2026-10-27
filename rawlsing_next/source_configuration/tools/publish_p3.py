"""Publish actual R157 P3 reader/key/loader validation results."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_read_admission import (
    CURRENT_GRANTED,
    EXACT_FILE,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceReaderConfiguration,
    decode_with_source_read_permission,
)
from rawlsing_next.source_configuration.factory import (
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.reader import (
    decode_config_with_source_read_permission,
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config

ROOT = Path(__file__).resolve().parents[3]
FOUNDATION = ROOT / "source_pre553_validation/foundation"
INTEGRATION = ROOT / "source_pre553_validation/integration"
P0_CONFIG = FOUNDATION / "examples/SRC09_q101_fixture.config.json"
P0_FIXTURE = FOUNDATION / "fixtures/SRC09_q101_nonrespondent.json"
P3_CONFIG = INTEGRATION / "examples/SRC09_q101_keyed_fixture.config.json"
R154_LOADER = ROOT / "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_load.py"
P0_TIP = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:r157:p3:probe:{tag}", semantic_hash({"tag": tag}))


class _Resolver:
    def __init__(self, *decisions):
        self.decisions = list(decisions)
        self.calls = 0

    def resolve_current(self, request):
        self.calls += 1
        return self.decisions[min(self.calls - 1, len(self.decisions) - 1)]


def _decision(request, **changes):
    material = dict(
        decision_ref=ref("DECISION", "d"),
        source_permission_refs=(ref("PERMISSION", "p"),),
        source_id=request.source_id, source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host, purpose=request.purpose, consumer_use=request.consumer_use,
        read_operation=SOURCE_RESPONSE_DECODE, physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-10-26/2026-10-27", currentness=CURRENT_GRANTED,
        revocation_ref=None, retention_export_limits={"export": "DENY", "retention": "SESSION"},
    )
    material.update(changes)
    return IssuedSourceReadDecision(**material)


def _reader_doc(sha256: str, fmt: str, encoding: dict | None = None):
    return {
        "identity": {
            "source_id": "SRC09", "expected_source_sha256": sha256, "source_format": fmt,
            "metadata_witness_ref": ref("METADATA_WITNESS", "m").as_dict(),
            "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": "P3_NONRESPONDENT_READER"},
            "reader": {
                "configuration_ref": ref("READER_CONFIGURATION", "r").as_dict(),
                "encoding": encoding,
            },
        },
        "binding": {"identity_class": "ORIGINAL_SOURCE"},
    }


def _read_probe(kind: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"p3_reader.{kind.lower()}"
        frame = pd.DataFrame({"ID": [1.0, 2.0], "X": [1.0, 0.0]})
        if kind == "SAV":
            pyreadstat.write_sav(frame, path)
        else:
            pyreadstat.write_dta(frame, path)
        source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        doc = _reader_doc(source_sha, kind)
        request = source_read_request_from_config(
            doc, host="p3-probe", purpose="R157_P3_PROBE",
            consumer_use="R157_P3_PROBE", semantic_use_scope=("R157_P3_PROBE",))
        resolver = _Resolver(_decision(request), _decision(request))
        incidence = decode_config_with_source_read_permission(
            doc, source_path=path, resolver=resolver, host="p3-probe",
            purpose="R157_P3_PROBE", consumer_use="R157_P3_PROBE",
            semantic_use_scope=("R157_P3_PROBE",))
        try:
            return {
                "format": kind,
                "source_sha256": incidence.source_sha256,
                "row_count": incidence.row_count,
                "reader_configuration": dict(incidence.reader_configuration),
                "resolver_calls": resolver.calls,
                "decision": "CURRENT_GRANTED",
                "original_source_execution": "NOT_PERFORMED",
            }
        finally:
            incidence.close()


def _key_probe() -> dict[str, Any]:
    cfg = load_source_config(P3_CONFIG)
    fixture = load_fixture_stream(P0_FIXTURE)
    keys = row_native_keys_from_transport(cfg, stream=fixture)
    release = build_validated_c11_release_from_config(cfg, stream=fixture)
    repository, release2 = build_source_backed_c11_repository_from_config(cfg, fixture)
    cells = (
        PhysicalCell(1, 124, "q101", 1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, 1, "country", 1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 124, "q101", 2.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 1, "country", None, PhysicalMissingState.SYSTEM_MISSING, None),
    )
    missing_stream = ExactPhysicalCellStream("f" * 64, 2, lambda: cells)
    missing_keys = row_native_keys_from_transport(cfg, stream=missing_stream)
    return {
        "config_path": str(P3_CONFIG.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(cfg),
        "fixture_source_sha256": fixture.source_sha256,
        "key_count": len(keys),
        "key_kind": keys[1].kind,
        "repeated_value_preserved": {
            "row_1_content_hash": keys[1].content_hash,
            "row_6_content_hash": keys[6].content_hash,
            "same_value_hash": keys[1].content_hash == keys[6].content_hash,
            "distinct_row_refs": keys[1].object_id != keys[6].object_id,
        },
        "missing_key_state": missing_keys[2].state,
        "release_ref": release.release_ref.as_dict(),
        "repository_release_ref": release2.release_ref.as_dict(),
        "repository_release_equal": release2.release_ref == release.release_ref,
        "repository_type": type(repository).__name__,
    }


def _load_r154():
    spec = importlib.util.spec_from_file_location("r157_p3_publish_r154_load", R154_LOADER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["r157_p3_publish_r154_load"] = module
    spec.loader.exec_module(module)
    return module


def _loader_probe() -> dict[str, Any]:
    module = _load_r154()
    # Avoid the historical private B49 module: the prepared path must not use it.
    module._b49 = lambda: (_ for _ in ()).throw(
        AssertionError("private B49 loader used by prepared path"))
    cfg = load_source_config(P0_CONFIG)
    keyed = load_source_config(P3_CONFIG)
    fixture = load_fixture_stream(P0_FIXTURE)
    base = module.build_native_workload("SRC09", config=cfg, source=fixture)
    keyed_result = module.build_native_workload("SRC09", config=keyed, source=fixture)
    wrong_cells = tuple(fixture.iter_cells())
    wrong = ExactPhysicalCellStream("f" * 64, 9, lambda: wrong_cells)
    try:
        module.build_native_workload("SRC09", config=cfg, source=wrong)
        refusal = None
    except Exception as exc:
        refusal = {"type": type(exc).__name__, "message": str(exc)}
    restored = module.build_native_workload("SRC09", config=cfg, source=fixture)
    partial = []
    for kwargs in ({"config": cfg}, {"source": fixture}):
        try:
            module.build_native_workload("SRC09", **kwargs)
        except Exception as exc:
            partial.append({"kwargs": sorted(kwargs), "type": type(exc).__name__, "message": str(exc)})
    return {
        "base": {
            "status": base.status,
            "issued_original_workload": base.issued_original_workload,
            "execution_permission_required": base.execution_permission_required,
            "release_ref": base.release.release_ref.as_dict(),
            "row_native_key_count": base.row_native_key_count,
            "native_calls": list(base.native_calls),
        },
        "keyed": {
            "release_ref": keyed_result.release.release_ref.as_dict(),
            "row_native_key_count": keyed_result.row_native_key_count,
        },
        "wrong_source_refusal": refusal,
        "restored_release_ref": restored.release.release_ref.as_dict(),
        "restore_matches_base": restored.release.release_ref == base.release.release_ref,
        "partial_input_refusals": partial,
        "b49_used": False,
    }


def _test_result() -> dict[str, Any]:
    command = [
        sys.executable, "-m", "pytest",
        "rawlsing_next/tests/test_source_configuration_foundation.py",
        "rawlsing_next/tests/test_source_configuration_p3.py",
        "rawlsing_next/tests/test_pre553_source_backed_c11_facade.py",
        "rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py",
        "rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py",
        "rawlsing_next/tests/test_pre553_source_read_admission.py",
        "rawlsing_next/tests/test_pre553_c11_repository_ingest.py",
        "-q", "-o", "addopts=",
    ]
    env = {**__import__("os").environ, "PYTHONPATH": str(ROOT)}
    done = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    tail = (done.stdout.strip().splitlines() or [""])[-1]
    return {
        "command": "PYTHONPATH=. " + " ".join(command[1:]),
        "returncode": done.returncode,
        "summary": tail,
        "stdout_tail": done.stdout.strip().splitlines()[-8:],
        "stderr_tail": done.stderr.strip().splitlines()[-8:],
        "passed": done.returncode == 0,
        "skipped": "skipped" in tail,
    }


def _legacy_r154_result() -> dict[str, Any]:
    command = [
        sys.executable, "-m", "pytest",
        "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/tests/test_r154_store.py",
        "-q", "-o", "addopts=",
    ]
    env = {**__import__("os").environ, "PYTHONPATH": str(ROOT)}
    done = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    tail = (done.stdout.strip().splitlines() or [""])[-1]
    return {
        "command": "PYTHONPATH=. " + " ".join(command[1:]),
        "returncode": done.returncode,
        "summary": tail,
        "known_limit": (
            "The legacy load_all/load_source path still imports the historical "
            "private .r61 B49 module, which is absent in this isolated checkout. "
            "The prepared P3 path deliberately bypasses _b49 and is tested with it disabled."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args()
    artifact_commit = args.artifact_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    base_cfg = load_source_config(P0_CONFIG)
    base_fixture = load_fixture_stream(P0_FIXTURE)
    base_release = build_validated_c11_release_from_config(base_cfg, stream=base_fixture)
    p3_cfg = load_source_config(P3_CONFIG)

    allowlisted_sha = next(iter(COMPATIBILITY_ALLOWLIST))
    encoding = COMPATIBILITY_ALLOWLIST[allowlisted_sha]
    qualified = SourceReaderConfiguration(
        allowlisted_sha, encoding, COMPATIBILITY_ONLY,
        configuration_ref=ref("READER_CONFIGURATION", "qualified"))
    try:
        SourceReaderConfiguration("a" * 64, "latin1", COMPATIBILITY_ONLY)
        unqualified = None
    except Exception as exc:
        unqualified = {"type": type(exc).__name__, "message": str(exc)}

    tests = _test_result()
    if not tests["passed"]:
        raise SystemExit(f"focused tests failed: {tests['summary']}\n{tests['stdout_tail']}")

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{P0_TIP}..{artifact_commit}"],
        cwd=ROOT, text=True).splitlines()
    changed_manifest = [{
        "path": path,
        "sha256": sha(ROOT / path),
        "bytes": (ROOT / path).stat().st_size,
    } for path in changed if (ROOT / path).is_file()]

    reader = {
        "qualified_allowlist_example": {
            "source_sha256": qualified.source_sha256,
            "encoding": qualified.encoding,
            "authority_status": qualified.authority_status,
            "configuration_ref": qualified.configuration_ref.as_dict(),
        },
        "unqualified_encoding_refusal": unqualified,
        "actual_decoder_probes": [_read_probe("SAV"), _read_probe("DTA")],
        "encoding_pass_through_test": "test_reader_encoding_is_passed_to_decoder_and_reader_sha_mismatch_refuses_before_resolver",
        "zero_io_before_permission": "unchanged; request/reader SHA checks precede resolver, decoder opens only after CURRENT_GRANTED",
    }
    keys = _key_probe()
    loader = _loader_probe()

    p3 = {
        "schema": "PYAT_R157_P3_RETURN@1.0.0",
        "task": "P3_READER_AND_ORIGINAL_BINDING",
        "status": "COMPLETE",
        "plan_seal": "4c0c619eac747afee1d8e65e1418bf2d472da4c3",
        "branch": "agent/pyat-pre553-r157-foundation",
        "p0_tip": P0_TIP,
        "artifact_commit": artifact_commit,
        "integration_branch": "agent/pyat-source-pre553-r157",
        "frozen_p0_interface": {
            "reused": True,
            "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
            "factory": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "factory_signature": "(config: SourceConfig | Mapping[str, Any], *, source_sha256: str | None = None, row_count: int | None = None, row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None) -> GovernedC11Projection",
            "no_signature_redesign": True,
        },
        "changed_artifacts": changed_manifest,
        "shared_seams": {
            "reader_transport": reader,
            "row_native_keys": keys,
            "r154_loader": loader,
        },
        "native_api_calls": [
            "rawlsing_next.source_configuration.reader.source_read_request_from_config",
            "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "rawlsing_next.pre553_physical_decoder.decode_sav / decode_dta",
            "rawlsing_next.source_configuration.factory.row_native_keys_from_transport",
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.pre553_source_backed_c11_facade.build_source_backed_c11_repository",
            "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_load.build_prepared_native_workload",
        ],
        "native_results": {
            "base_fixture_release_ref": base_release.release_ref.as_dict(),
            "keyed_fixture_release_ref": keys["release_ref"],
            "base_release_is_c11_logical_release": isinstance(base_release, C11LogicalRelease),
            "keyed_repository_release_matches": keys["repository_release_equal"],
            "loader_prepared_release_ref": loader["base"]["release_ref"],
            "loader_restore_matches_base": loader["restore_matches_base"],
        },
        "before_after": {
            "before_p3_r154_loader": "unconditional build_native_workload refusal; no prepared config-to-native path",
            "after_p3_r154_loader": "with exact config + permitted transport it delegates to the existing C11 owner; without both it preserves CURRENT_SOURCE_READ_GRANT_REQUIRED / explicit prepared-input refusal",
            "wrong_source_then_restore": {
                "refusal": loader["wrong_source_refusal"],
                "restored_release_ref": loader["restored_release_ref"],
                "restore_matches_base": loader["restore_matches_base"],
            },
            "reader_unqualified_then_qualified": {
                "unqualified_refusal": unqualified,
                "qualified_example": reader["qualified_allowlist_example"],
            },
        },
        "tests": tests,
        "legacy_r154_suite": _legacy_r154_result(),
        "lane_compatibility": {
            "source_lanes_may_continue": True,
            "lane_data_directories_not_modified": True,
            "reader_rule": "Set identity.reader.encoding only for the exact source SHA present in COMPATIBILITY_ALLOWLIST; otherwise leave null. No guessing/fallback.",
            "key_rule": "Configure respondents.source_native_key_slot; wrapper auto-populates exact row_native_keys from permitted decoded cells. Missing cells become TypedAbsence(UNKNOWN), never invented keys.",
            "original_vs_fixture": "Original configs keep original identity/authority; fixture configs keep distinct fixture SHA and fixture-only authority.",
            "existing_commands": [
                "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p0",
                "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p3",
            ],
        },
        "scope_limits": [
            "No original respondent rows or original source file bytes read.",
            "No original empirical workload issuance or execution permission is created.",
            "No all35 source configs were authored or overwritten; source-lane directories are untouched.",
            "No FieldForge/M1/N11/N12/CI/prod/Sorok/J52W52 scope.",
            "The legacy R154 load_source B49 path still requires the historical private module; prepared construction deliberately bypasses it. P5 must pin/vendor that legacy dependency if the legacy loader is to remain portable.",
        ],
        "next_consumer": "HQ / P4 source lanes; use frozen P0 config schema and P3 reader/key wrappers, then return lane configs and native fixture traces.",
    }
    INTEGRATION.mkdir(parents=True, exist_ok=True)
    (INTEGRATION / "P3_RETURN.json").write_text(
        json.dumps(p3, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "artifact_commit": artifact_commit,
        "tests": tests["summary"],
        "base_release": base_release.release_ref.as_dict(),
        "keyed_release": keys["release_ref"],
        "loader_status": loader["base"]["status"],
        "p3_return": str(INTEGRATION / "P3_RETURN.json"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
