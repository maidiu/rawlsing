#!/usr/bin/env python3
"""Targeted assertion mutation and restoration check (disposable copy only)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_probes_r2 as probes  # noqa: E402

MUTANT_PATH = (HERE.parent / "mutants" /
               "universal_runner_verify_mutant_disable_result_check.py")
intact = probes.verify
spec = importlib.util.spec_from_file_location("r09v_r2_mutant", MUTANT_PATH)
mutant = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mutant
spec.loader.exec_module(mutant)

WRONG_ENTRY = (
    "from native_fixture import add, double\n"
    "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1)) - 1}\n"
)


def run(module, name: str) -> dict:
    probes.verify = module
    fixture = probes.Fixture(name, entry=WRONG_ENTRY)
    observation = fixture.observe()
    decision = fixture.decision(observation)
    fixture.cleanup()
    return {
        "decision": decision.get("decision"),
        "reasons": decision.get("reasons"),
        "observed_result": decision.get("observed", {}).get("result"),
    }


result = {
    "mutant_path": str(MUTANT_PATH),
    "mutant_sha256": probes.sha_bytes(MUTANT_PATH.read_bytes()),
    "intact_verifier_sha256": probes.sha_bytes(
        probes.MODULE_PATH.read_bytes()),
    "intact": run(intact, "mutant-intact"),
    "mutant": run(mutant, "mutant-disabled"),
}
probes.verify = intact
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if (
    result["intact"]["decision"] == intact.REFUSE
    and "RESULT_MISMATCH" in (result["intact"]["reasons"] or [])
    and result["mutant"]["decision"] == mutant.ACCEPT
) else 1)
