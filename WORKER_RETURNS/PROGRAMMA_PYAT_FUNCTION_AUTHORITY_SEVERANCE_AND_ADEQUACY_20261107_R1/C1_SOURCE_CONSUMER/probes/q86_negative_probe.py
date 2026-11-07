#!/usr/bin/env python3
"""Sourcefree negative/restoration controls at the real Q86 I03 first reader."""
from __future__ import annotations

import json
import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

import rawlsing_next.wave1_gt12_i03_positive_facts as gt12b
from rawlsing_next.tests.test_wave1_gt12_i03_positive_facts import _fixture

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C1_SOURCE_CONSUMER"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(name, fn):
    try:
        fn()
    except Exception as exc:  # expected typed negative
        return {"case": name, "result": "TYPED_REFUSAL", "exception": type(exc).__name__, "message": str(exc)[:300]}
    return {"case": name, "result": "UNEXPECTED_ACCEPT"}


def main() -> int:
    import re
    module_text = (ROOT / "rawlsing_next/wave1_gt12_i03_positive_facts.py").read_text(encoding="utf-8")
    production_source = re.search(r'^FROZEN_R5_SOURCE_SHA256\s*=\s*"([0-9a-f]{64})"', module_text, re.MULTILINE)
    production_source_sha = production_source.group(1) if production_source else None
    mp = pytest.MonkeyPatch()
    try:
        source, release, binding, registry, _, _, _ = _fixture(mp)
        frozen = {
            "FROZEN_R5_SOURCE_SHA256": gt12b.FROZEN_R5_SOURCE_SHA256,
            "FROZEN_RISK_SET_MEMBER_COUNT": gt12b.FROZEN_RISK_SET_MEMBER_COUNT,
            "FROZEN_RISK_MEMBER_SET_SHA256": gt12b.FROZEN_RISK_MEMBER_SET_SHA256,
        }
        baseline = gt12b.execute_gt12b_i03_plan(
            release=release,
            plan=gt12b.build_gt1_q86a_i03_plan(release=release, binding=binding, authority_registry=registry),
            authority_registry=registry,
        )
        baseline_record = {
            "typed_state": baseline.fact.typed_state,
            "raw_numerator_support": baseline.fact.raw_numerator_support,
            "raw_denominator_support": baseline.fact.raw_denominator_support,
        }

        cases = []
        cases.append(run_case("wrong_source_sha", lambda: (
            setattr(gt12b, "FROZEN_R5_SOURCE_SHA256", "0" * 64),
            gt12b.build_gt1_q86a_i03_plan(release=release, binding=binding, authority_registry=registry),
        )))
        setattr(gt12b, "FROZEN_R5_SOURCE_SHA256", frozen["FROZEN_R5_SOURCE_SHA256"])
        cases.append(run_case("wrong_qimpl", lambda: gt12b.build_gt1_q86a_i03_plan(
            release=release,
            binding=replace(binding, q86a=replace(binding.q86a, question_impl_id="question_impl.phase0.wrong")),
            authority_registry=registry,
        )))
        cases.append(run_case("wrong_source_structure_wave_grain", lambda: gt12b.build_gt1_q86a_i03_plan(
            release=release,
            binding=replace(binding, q86a=replace(binding.q86a, current_source_structure_id="cssu.r1.afrobarometer.r9.wrong")),
            authority_registry=registry,
        )))
        cases.append(run_case("wrong_risk_set_count", lambda: (
            setattr(gt12b, "FROZEN_RISK_SET_MEMBER_COUNT", 2),
            gt12b.build_gt1_q86a_i03_plan(release=release, binding=binding, authority_registry=registry),
        )))
        setattr(gt12b, "FROZEN_RISK_SET_MEMBER_COUNT", frozen["FROZEN_RISK_SET_MEMBER_COUNT"])
        cases.append(run_case("wrong_target_use_operation", lambda: gt12b.build_gt1_q86a_i03_plan(
            release=release,
            binding=replace(binding, gt1_target_use=replace(binding.gt1_target_use, operation="WRONG-TARGET-USE-OPERATION")),
            authority_registry=registry,
        )))
        cases.append(run_case("wrong_permission_ceiling", lambda: gt12b.build_gt1_q86a_i03_plan(
            release=release,
            binding=replace(binding, gt1_target_use=replace(binding.gt1_target_use, permission_ceiling="GENERAL_STRUCTURAL_OR_ACTOR_USE")),
            authority_registry=registry,
        )))
        # Restoration: exact baseline must still run after all mutations are undone.
        restore = gt12b.execute_gt12b_i03_plan(
            release=release,
            plan=gt12b.build_gt1_q86a_i03_plan(release=release, binding=binding, authority_registry=registry),
            authority_registry=registry,
        )
        result = {
            "schema": "C1_Q86_NEGATIVE_RESTORATION_PROBE_V1",
            "sourcefree_fixture": True,
            "selected_contract_hash_binding_test": {
                "result": "NOT_RUN",
                "blocker": "current Q86 operation and fixture do not bind AR-0033 selected response_semantics_contract_hash; no legal actual selected-version fixture exists in this lease",
            },
            "baseline": baseline_record,
            "cases": cases,
            "restoration_pass": restore.fact.typed_state == baseline.fact.typed_state and restore.fact.raw_denominator_support == baseline.fact.raw_denominator_support,
            "module_sha256": sha256(ROOT / "rawlsing_next/wave1_gt12_i03_positive_facts.py"),
            "production_frozen_source_sha256": production_source_sha,
            "fixture_source_sha256": gt12b.FROZEN_R5_SOURCE_SHA256,
            "seed": "PYTHONHASHSEED=0",
        }
        (OUT / "probes/q86_negative_probe.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    finally:
        mp.undo()


if __name__ == "__main__":
    raise SystemExit(main())
