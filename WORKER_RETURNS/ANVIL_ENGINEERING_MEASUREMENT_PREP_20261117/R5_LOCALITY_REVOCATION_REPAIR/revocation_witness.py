#!/usr/bin/env python3
"""R4 RED vs R5 GREEN CURRENT-between-yields witness on sealed R2 estate."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT / "vendor"))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

CONTRACT = ROOT / "R2_PILOT" / "fixture_contract_pilot.json"
R4_ADAPTER = ROOT / "R4_LOCALITY_EXPERIMENT" / "locality_adapter.py"
R5_ADAPTER = HERE / "locality_adapter.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _estate(contract, grant):
    e = contract["estate"]
    return VerifiedDirectEstate(
        e["root"], exact_path=e["exact_path"],
        independently_held_manifest_sha256=e["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**e["i02"]),
        current_authorizer=lambda _roots: grant["ok"],
    )


def _adapter_case(adapter_mod, contract, grant):
    original = adapter_mod.install()
    try:
        estate = _estate(contract, grant)
        with DirectEstateI03Session(estate) as session:
            respondent = next(iter(session.respondents))
            gen = session._respondent_family("RoutingEligibilityFact", respondent)
            first = next(gen)
            first_ref = first.ref.key
            grant["ok"] = False
            try:
                second = next(gen)
                error = None
                second_ref = second.ref.key
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                second_ref = None
    finally:
        adapter_mod.restore(original)
    return {
        "first_ref": first_ref,
        "second_ref": second_ref,
        "second_error": error,
        "bypassed": error is None and second_ref is not None,
        "restored": DirectEstateI03Session._respondent_family is original,
    }


def _original_case(contract, grant):
    estate = _estate(contract, grant)
    with DirectEstateI03Session(estate) as session:
        respondent = next(iter(session.respondents))
        gen = session._respondent_family("RoutingEligibilityFact", respondent)
        first = next(gen)
        first_ref = first.ref.key
        grant["ok"] = False
        try:
            second = next(gen)
            error = None
            second_ref = second.ref.key
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            second_ref = None
    return {
        "first_ref": first_ref,
        "second_ref": second_ref,
        "second_error": error,
        "refused": error is not None,
    }


def _valid_order(adapter_mod, contract, grant):
    # Product original order, then corrected adapter order, same respondent.
    grant["ok"] = True
    estate = _estate(contract, grant)
    with DirectEstateI03Session(estate) as session:
        respondent = next(iter(session.respondents))
        original_refs = [
            obj.ref.key for obj in session._respondent_family(
                "RoutingEligibilityFact", respondent)
        ]
    original = adapter_mod.install()
    try:
        estate2 = _estate(contract, grant)
        with DirectEstateI03Session(estate2) as session2:
            respondent2 = next(iter(session2.respondents))
            corrected_refs = [
                obj.ref.key for obj in session2._respondent_family(
                    "RoutingEligibilityFact", respondent2)
            ]
    finally:
        adapter_mod.restore(original)
    return {
        "count": len(corrected_refs),
        "canonical_sorted": corrected_refs == sorted(corrected_refs),
        "matches_original_order": corrected_refs == original_refs,
        "first_ref": corrected_refs[0] if corrected_refs else None,
        "last_ref": corrected_refs[-1] if corrected_refs else None,
        "restored": DirectEstateI03Session._respondent_family is original,
    }


def main() -> int:
    contract = json.loads(CONTRACT.read_text())
    grant = {"ok": True}
    r4 = _load("r4_locality_adapter", R4_ADAPTER)
    r5 = _load("r5_locality_adapter", R5_ADAPTER)

    grant["ok"] = True
    red = _adapter_case(r4, contract, grant)
    grant["ok"] = True
    green = _adapter_case(r5, contract, grant)
    grant["ok"] = True
    original = _original_case(contract, grant)
    grant["ok"] = True
    order = _valid_order(r5, contract, grant)
    witness = {
        "schema": "ANVIL_CUT2_R5_LOCALITY_REVOCATION_REPAIR_WITNESS@1",
        "sealed_estate_manifest": contract["estate"]["manifest_sha256"],
        "family": "RoutingEligibilityFact",
        "r4_red": red,
        "r5_green": green,
        "original_control": original,
        "valid_iteration_order": order,
        "red_expected": red["bypassed"] is True,
        "green_expected": green["bypassed"] is False and "current source/operation authority refused" in (green["second_error"] or ""),
        "original_expected": original["refused"] is True,
        "order_expected": order["canonical_sorted"] and order["matches_original_order"] and order["count"] > 0,
        "all_expected": False,
    }
    witness["all_expected"] = all((
        witness["red_expected"], witness["green_expected"],
        witness["original_expected"], witness["order_expected"],
        red["restored"], green["restored"], order["restored"],
    ))
    (HERE / "revocation_witness.json").write_text(
        json.dumps(witness, indent=2, sort_keys=True) + "\n")
    print(json.dumps(witness, indent=2, sort_keys=True))
    return 0 if witness["all_expected"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
